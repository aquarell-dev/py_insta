from libs.instagram_spammer import InstagramSpammer
from libs.instagram import Instagram
from config import user_config

if __name__ == '__main__':
    print('[+] Process started...')
    Instagram.execute(InstagramSpammer, user_config.LOGIN, user_config.PASSWORD, user_config.TARGET_LINK)
    print('[+] Process has been stopped.')
