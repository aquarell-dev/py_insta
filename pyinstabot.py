from libs.instagram import Instagram
from config import user_config

if __name__ == '__main__':
    instagram = Instagram(
        login=user_config.LOGIN,
        password=user_config.PASSWORD
    )
