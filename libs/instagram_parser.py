import math
from typing import Optional, List, Tuple
import httpx
import json
import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import user_config, dev_config
from libs.instagram import Instagram
from libs import ie
from libs.json_ import write_file

class InstagramParser(Instagram):
    def __init__(self, login: str, password: str, target: str):
        super().__init__(login, password, target)
        self._cookies = httpx.Cookies()
        self._username = user_config.TARGET_LINK.split('/')[-2]

    _httpxErrors = (
        httpx.HTTPError,
        httpx.InvalidURL,
        httpx.CookieConflict,
        httpx.StreamError
    )

    def perform(self) -> None:
        """ Goes on a user page and grabs his followers and stores it into json. """
        self._set_cookies()

        target_id = self._get_target_user_id()

        if target_id is None:
            print(f'[-] Couldn\'t get the target user\'s id.')
            return

        print(f'[+] Target id: {target_id}.')

        try:
            followers_count = user_config.FOLLOWERS_COUNT
        except ie.LoadingError:
            print('[-] Couldn\'t get followers count.')
            return
        except ValueError:
            print('[-] Couldn\'t parse followers count.')
            return

        print(f'[+] Found total {followers_count} followers.')

        self._driver.quit()

        parsed_followers = self._parse_followers(target_id, followers_count)

        file_path = os.path.join(dev_config.FOLLOWERS_FOLDER, f'followers-{self._username}.json')

        write_file(
            data=parsed_followers,
            file=file_path
        )

        print(f'[+] Successfully save the file. Path: {file_path}.')

    def _set_cookies(self) -> None:
        for cookie in self._driver.get_cookies():
            self._cookies.set(cookie['name'], cookie['value'])

    def _get_target_user_id(self) -> Optional[int]:
        """
        Gets target user id.
        Id is required to execute get requests to the api.
        """
        if not self._safe_get(user_config.TARGET_LINK):
            return None

        content = self._driver.find_element(By.XPATH, '//body//script').get_attribute(
            'innerHTML'
        ).split(' = ')[-1].replace(';', '')

        try:
            return int(json.loads(content)['entry_data']['ProfilePage'][0]['graphql']['user']['id'])
        except (KeyError, ValueError):
            return None

    def _get_first_max_id(self, target_id) -> str:
        """ Sometimes instagram """
        return httpx.get(
            f'https://i.instagram.com/api/v1/friendships/{target_id}/followers/?count=1',
            headers={
                'user-agent': 'Instagram 219.0.0.12.117 Android'
            },
            cookies=self._cookies
        ).json()['next_max_id']

    def _parse_followers(self, target_id: int, followers_count: int) -> dict:
        global_followers = {}

        requests_count = 0

        step = 100

        total_requests = math.floor(followers_count / step)

        max_id = self._get_first_max_id(target_id)

        for i in range(step, followers_count, step):
            try:
                followers, next_max_id = self._get_followers(target_id, max_id, step)
            except self._httpxErrors:
                print(f'[-] Couldn\'t get next {step} followers.')
                continue

            max_id = next_max_id

            requests_count += 1

            current_followers = {
                str(follower['username']): {
                    "link": f"https://www.instagram.com/{follower['username']}/",
                    "done": False,
                }
                for follower in followers if not follower['is_private']
            }

            global_followers.update(current_followers)

            print(
                f'[+] Collected {len(current_followers)} new users. '
                f'Total collected: {len(global_followers)}. '
                f'Requests made: {requests_count} out of {total_requests}.'
            )

        return global_followers

    def _get_followers(self, target_id: int, max_id: str, step: int) -> Tuple[List[dict], str]:
        """
        NOTE. I could've used async, but time is almost up, so
        :param target_id:
        :param max_id:
        :param step:
        :return:
        """
        response = httpx.get(
            f'https://i.instagram.com/api/v1/friendships/{target_id}/followers/?count={step}&max_id={max_id}&search_surface=follow_list_page',
            headers={
                'user-agent': 'Instagram 219.0.0.12.117 Android'
            },
            cookies=self._cookies
        ).json()

        return response['users'], response['next_max_id']
