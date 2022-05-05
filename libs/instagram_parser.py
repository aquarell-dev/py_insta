from libs.instagram import Instagram


class InstagramParser(Instagram):
    def _perform(self) -> None:
        """ Goes on a user page and grabs his followers. """
