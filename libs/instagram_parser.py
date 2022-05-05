from typing import Tuple, Optional

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import user_config
from libs.instagram import Instagram, random_sleep
from libs import ie

import requests

import httpx

import json

class InstagramParser(Instagram):
    def __init__(self, login: str, password: str, target: str):
        super().__init__(login, password, target)
        self._session = requests.Session()
        self._cookies = httpx.Cookies()

    def perform(self) -> None:
        """ Goes on a user page and grabs his followers. """
        followers = dict()

        self._set_cookies()

        target_id = self._get_target_user_id()

        if target_id is None: return

        self._driver.quit()

        r = httpx.get(
            'https://i.instagram.com/api/v1/friendships/49810841459/followers/?count=12&search_surface=follow_list_page',
            headers={
                'user-agent': 'Instagram 219.0.0.12.117 Android'
            },
            cookies=self._cookies
        )

        print(r.content)

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
        print(json.loads(content)['entry_data']['graphql']['user']['id'])
        return 0

    def _update_followers(self) -> None:
        """ Updates the dict with followers. """
