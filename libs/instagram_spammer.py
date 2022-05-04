from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import user_config
from libs.instagram import Instagram, random_sleep
from libs import ie

class InstagramSpammer(Instagram):
    def perform(self) -> None:
        """
        Loops through the users, subscribes to them, likes their posts,
        and messages them.
        :return:
        """
        for idx, user in self._users.items():
            url = user['link']

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

            print(f'[+] Followed to {url}.')

            try:
                posts = self._like_posts()
            except ie.LoadingError:
                print(f'[-] Not able to load the posts. User: {url}.')
                continue

            print(f'[+] Liked {url} posts.')

            self._direct_message()

            print(f'[+] User: {url}. Subscribed. Posts liked: {posts}. Messaged.')

    def _subscribe(self) -> None:
        """ Subscribes to a user. """
        locators = {
            'follow': (By.XPATH, '//button//div[.="Follow"]/..'),
        }

        if self._is_acc_private():
            raise ie.AccountPrivate()

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

    def _like_posts(self) -> int:
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

        if not posts:
            return liked_posts

        for idx, post in enumerate(posts):
            self._ac.move_to_element(post).click().perform()

            try:
                self._wait.until(EC.element_to_be_clickable(locators['like']))
                self._wait.until(EC.element_to_be_clickable(locators['exit']))
            except TimeoutException:
                print(f'[-] Couldn\'t load post.')
                continue

            self._driver.find_element(*locators['like']).click()

            random_sleep()

            self._driver.find_element(*locators['exit']).click()

            random_sleep()

            liked_posts += 1

            if idx == 3: break

        return liked_posts

    def _direct_message(self, message: str = user_config.MESSAGE) -> None:
        """ Messages a user. """
        locators = {
            'message': (By.XPATH, '//button[@type="button"]//div[.="Message"]/..')
        }

        try:
            self._wait.until(EC.element_to_be_clickable(locators['message']))
        except TimeoutException:
            raise ie.LoadingError()

        message_button = self._driver.find_element(*locators['message'])

        self._ac.move_to_element(message_button).click().perform()

        random_sleep()
