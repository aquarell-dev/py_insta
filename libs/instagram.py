from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.common import exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from libs import ie
from libs.json_ import read_file
from libs.core import Core, Docker, Proxy
from config import dev_config, user_config
import time, os
import random

def random_sleep() -> None:
    n = random.randint(4, 8)
    print(f'[+] Sleeping for {n} seconds...')
    time.sleep(n)

class Instagram:
    def __init__(self, login: str, password: str, target: str) -> None:
        """
        :param login - user login:
        :param password - user password:
        :param target - instagram link to the target profile:
        """
        self._login = login
        self._password = password

        self._target = target

        self._driver = Core(executable_path=dev_config.CHROMEDRIVER).initialize_driver()
        # self._driver = Docker().initialize_driver()
        # self._driver = Proxy(executable_path=dev_config.CHROMEDRIVER, proxy=dev_config.PROXY).initialize_driver()

        self._wait = WebDriverWait(self._driver, 10)
        self._ac = ActionChains(self._driver)

        self._users = read_file(os.path.join(dev_config.FOLLOWERS_FOLDER, user_config.FOLLOWERS_FILE))

    def __repr__(self) -> str:
        return repr(f'Account. Login - {self._login}.')

    def login(self) -> None:
        if not self._safe_get('https://instagram.com'):
            self._driver.quit()
            raise ConnectionError('Couldn\'t connect to instagram.')

        locators = {
            'login': (By.XPATH, '//input[@name="username"]'),
            'pass': (By.XPATH, '//input[@name="password"]'),
            'submit': (By.XPATH, '//button[@type="submit"]/..'),
            'cookies': (By.XPATH, '//div[@role="dialog"]')
        }

        try:
            self._wait.until(EC.presence_of_element_located(locators['login']))
            self._wait.until(EC.presence_of_element_located(locators['pass']))
            self._wait.until(EC.presence_of_element_located(locators['submit']))
        except TimeoutException:
            self._driver.quit()
            raise ie.LoadingError('Couldn\'t load the page.')

        self._accept_cookies()

        # instagram protects itself for real incredibly so i added these random time sleeps
        self._driver.find_element(*locators['login']).send_keys(self._login)

        random_sleep()

        self._driver.find_element(*locators['pass']).send_keys(self._password)

        random_sleep()

        self._driver.find_element(*locators['submit']).click()

        if not self._does_element_exist((By.XPATH, '//div[@class="olLwo"]')):
            self._driver.quit()
            raise ie.AuthorizationError(f'Couldn\'t log in. {self._login}')

        self._accept_cookies()

    def _accept_cookies(self) -> None:
        if self._does_element_exist((By.XPATH, '//div[@role="dialog"]')):
            self._driver.find_element(By.XPATH, '//button[@tabindex=0]').click()
            time.sleep(5)

    def _does_element_exist(self, locator) -> bool:
        """ Returns True if element exists or else False. """
        try:
            self._wait.until(
                EC.presence_of_element_located(
                    locator
                )
            )
        except (exceptions.TimeoutException, exceptions.StaleElementReferenceException):
            return False

        return True

    def _safe_get(self, url: str) -> bool:
        """ Goes to the page or else throws an error. """
        try:
            self._driver.get(url)
        except WebDriverException:
            return False

        return True
