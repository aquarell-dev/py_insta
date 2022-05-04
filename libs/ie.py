class LoadingError(RuntimeError):
    pass

class AuthorizationError(RuntimeError):
    pass

class AccountPrivate(RuntimeError):
    pass

class NoPostsError(RuntimeError):
    pass

class AlreadySubscribed(RuntimeError):
    pass
