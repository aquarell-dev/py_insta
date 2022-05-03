from config import user_config
from libs.instagram import Instagram
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

            self._subscribe()

            self._like_posts()

            self._direct_message()

    def _subscribe(self) -> None:
        """ Subscribes to a user. """

    def _is_acc_private(self) -> bool:
        pass

    def _like_posts(self) -> None:
        """ Likes a user's three latest posts. """

    def _direct_message(self, message: str = user_config.MESSAGE) -> None:
        """ Messages a user. """
        pass
