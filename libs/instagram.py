from selenium.common.exceptions import WebDriverException
from selenium.common import exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from libs.core import Core, Docker, Proxy
from config import dev_config
import time

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

        # self._driver = Core(executable_path=dev_config.CHROMEDRIVER).initialize_driver()
        # self._driver = Docker().initialize_driver()
        self._driver = Proxy(executable_path=dev_config.CHROMEDRIVER, proxy=dev_config.PROXY).initialize_driver()

        self._wait = WebDriverWait(self._driver, 10)
        self._ac = ActionChains(self._driver)

    def __repr__(self) -> str:
        return repr(f'Account. Login - {self._login}.')

    def login(self) -> None:
        time.sleep(1000)
        if not self._sage_get('https://instagram.com'):
            self._driver.quit()
            raise ConnectionError('Couldn\'t connect to instagram.')

        locators = {
            'login': (By.XPATH, ''),
            'pass': (By.XPATH, ''),
            'submit': (By.XPATH, ''),
            'confirm_login': (By.XPATH, '')
        }

        try:
            self._wait.until(EC.presence_of_element_located(locators['login']))
            self._wait.until(EC.presence_of_element_located(locators['pass']))
            self._wait.until(EC.presence_of_element_located(locators['submit']))
        except WebDriverException:
            self._driver.quit()
            raise RuntimeError('Couldn\'t load login button.')

        self._driver.find_element(locators['login']).send_keys(self._login)
        self._driver.find_element(locators['pass']).send_keys(self._password)
        self._driver.find_element(locators['submit']).click()

        if self._does_element_exist(locators['confirm_login']):
            self._driver.quit()
            raise RuntimeError('Authentication error.')

    def like_posts(self) -> None:
        """ Likes the three latest user's posts. """

    def subscribe(self) -> None:
        """ Subscribes to a user. """
        pass

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

    def _sage_get(self, url: str) -> bool:
        """ Goes to the page or else throws an error. """
        try:
            self._driver.get(url)
        except WebDriverException:
            return False

        return True
