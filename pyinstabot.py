from libs.instagram_spammer import InstagramSpammer
from libs import ie
from config import user_config

def main():
    instagram = InstagramSpammer(
        login=user_config.LOGIN,
        password=user_config.PASSWORD,
        target=user_config.TARGET_LINK
    )

    print('[+] Logging in...')

    try:
        instagram.login()
    except ConnectionError:
        print('[-] Couldn\'t establish connection.')
        return
    except ie.LoadingError:
        print('[-] Couldn\'t load the page.')
        return
    except ie.AuthorizationError:
        print('[-] Couldn\'t log in.')
        return

    print('[+] Connection to Instagram has been established.')

    instagram.perform()

if __name__ == '__main__':
    print('[+] Process started...')
    main()
    print('[+] Process has been stopped.')
