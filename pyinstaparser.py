from libs.instagram_parser import InstagramParser
from libs.instagram import Instagram
from config import user_config
from libs.json_ import read_file
if __name__ == '__main__':
    print('[+] Process started...')
    Instagram.execute(InstagramParser, user_config.LOGIN, user_config.PASSWORD, user_config.TARGET_LINK)
    print('[+] Process has been stopped.')
