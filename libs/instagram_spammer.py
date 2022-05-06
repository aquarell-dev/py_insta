from typing import Tuple
import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import user_config, dev_config
from libs.instagram import Instagram, random_sleep
from libs import ie
from libs.json_ import read_file, validate_json, write_file


class InstagramSpammer(Instagram):
    def __init__(self, login: str, password: str, target: str) -> None:
        super().__init__(login, password, target)
        self._users_path = os.path.join(dev_config.FOLLOWERS_FOLDER, user_config.FOLLOWERS_FILE)
        self._users = validate_json(
            read_file(self._users_path),
            user_config.USERS_COUNT
        )

    def perform(self) -> None:
        """
        Loops through the users, subscribes to them, likes their posts,
        and messages them.
        :return:
        """
        new_users = {}

        for idx, user in self._users.items():
            url = user['link']

            print(f'[+] User: {url}({idx} out of {len(self._users)}).')

            if not self._safe_get(url):
                print(f'[-]. Couldn\'t load the user\'s page. User: {url}.')
                continue

            try:
                self._subscribe()
            except ie.AccountPrivate:
                print(f'[-] Account is private. User: {url}.')
                continue
            except ie.LoadingError:
                print(f'[-] Not able to load the subscribe button. User: {url}.')
                continue
            except ie.AlreadySubscribed:
                print(f'[+] Already subscribed to {url}.')
            else:
                print(f'[+] Followed to {url}.')

            try:
                posts, liked_posts = self._like_posts()
            except ie.LoadingError:
                print(f'[-] Not able to load the posts. User: {url}.')
                continue
            else:
                if liked_posts > 0:
                    print(f'[+] {liked_posts} of {url} posts has(ve) been already liked.')
                print(f'[+] Liked {posts} post(s) of {url}.')

            try:
                self._direct_message()
            except ie.LoadingError:
                print(f'[-] Not able to locate the message button. Mb you ain\'t allowed to message them.')
            else:
                print(f'[+] Message to {url} has been sent.')

            new_users.update({})

        self._update_followers(new_users)

    def _subscribe(self) -> None:
        """ Subscribes to a user. """
        locators = {
            'follow': (By.XPATH, '//button//div[.="Follow"]/..'),
        }

        if self._is_acc_private():
            raise ie.AccountPrivate()

        if self._is_already_subscribed():
            raise ie.AlreadySubscribed()

        try:
            self._wait.until(EC.presence_of_element_located(locators['follow']))
        except TimeoutException:
            raise ie.LoadingError()

        random_sleep()

        self._driver.find_element(*locators['follow']).click()

        random_sleep()

    def _is_acc_private(self) -> bool:
        try:
            self._wait.until(EC.presence_of_element_located((By.XPATH, '//h2[@class="rkEop" and .="This Account is Private"]')))
        except TimeoutException:
            return False

        return True

    def _is_already_subscribed(self) -> bool:
        try:
            self._wait.until(EC.presence_of_element_located(
                (By.XPATH, '//button//div//div//*[name()="svg" and @aria-label="Following"]')
            ))
        except TimeoutException:
            return False

        return True

    def _like_posts(self) -> Tuple[int, int]:
        """ Likes a user's three latest posts. """
        locators = {
            'posts': (By.CLASS_NAME, 'v1Nh3'),
            'like': (By.XPATH, '//button//span//*[name()="svg" and @aria-label="Like"]'),
            'exit': (By.XPATH, '//button//div//*[name()="svg" and @aria-label="Close"]')
        }

        try:
            self._wait.until(EC.presence_of_element_located(locators['posts']))
        except TimeoutException:
            raise ie.LoadingError()

        posts = self._driver.find_elements(*locators['posts'])

        liked_posts = 0
        already_liked = 0

        if not posts:
            return liked_posts, 0

        for idx, post in enumerate(posts):
            self._ac.move_to_element(post).click().perform()

            try:
                self._wait.until(EC.element_to_be_clickable(locators['exit']))
            except TimeoutException:
                continue

            if not self._is_already_liked():
                self._driver.find_element(*locators['like']).click()
                liked_posts += 1
                random_sleep()
            else:
                already_liked += 1

            self._driver.find_element(*locators['exit']).click()

            random_sleep()

            if idx == 2: break

        return liked_posts, already_liked

    def _is_already_liked(self) -> bool:
        try:
            self._wait.until(EC.presence_of_element_located(
                (By.XPATH, '//button//div//span//*[name()="svg" and @aria-label="Unlike"]')
            ))
        except TimeoutException:
            return False

        return True

    def _direct_message(self, message: str = user_config.MESSAGE) -> None:
        """ Messages a user. """
        locators = {
            'message': (By.XPATH, '//button[@type="button"]//div[.="Message"]/..'),
            'textarea': (By.TAG_NAME, 'textarea')
        }

        try:
            self._wait.until(EC.element_to_be_clickable(locators['message']))
        except TimeoutException:
            raise ie.LoadingError()

        message_button = self._driver.find_element(*locators['message'])

        self._ac.move_to_element(message_button).click().perform()

        random_sleep()

        try:
            self._wait.until(EC.presence_of_element_located(locators['textarea']))
        except TimeoutException:
            return

        message_input = self._driver.find_element(*locators['textarea'])

        message_input.send_keys(message)

        message_input.send_keys(Keys.RETURN)

    def _update_followers(self, users: dict) -> bool:
        """ Takes the new followers and updates the .json file. """
        old_users = read_file(self._users_path)

        old_users.update(users)

        write_file(old_users, self._users_path)

        return True
