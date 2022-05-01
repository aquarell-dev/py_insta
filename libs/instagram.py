from libs.core import Standard, Docker, Proxy

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

    def login(self) -> bool:
        pass

    def _like_posts(self) -> None:
        """ Likes the three latest user's posts. """

    def _subscribe(self) -> None:
        """ Subscribes to a user. """
        pass

    def _sage_get(self) -> None:
        """ Goes to the page or else throws an error. """
        # try:
        #     self.driver.get(self._target)
        # except selenium.exceptions.DriverException as e:
        #     return False
        #
        # return True
