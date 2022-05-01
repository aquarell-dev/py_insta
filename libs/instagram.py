from selenium.common.exceptions import WebDriverException
from libs.core import Core, Docker, Proxy
from config import dev_config

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

    def login(self) -> None:
        if not self._sage_get('https://instagram.com'):
            raise ConnectionError('Couldn\'t connect to instagram.')

    def _like_posts(self) -> None:
        """ Likes the three latest user's posts. """

    def _subscribe(self) -> None:
        """ Subscribes to a user. """
        pass

    def _sage_get(self, url: str) -> bool:
        """ Goes to the page or else throws an error. """
        try:
            self._driver.get(url)
        except WebDriverException:
            return False

        return True
