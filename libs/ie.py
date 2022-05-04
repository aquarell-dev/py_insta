class LoadingError(RuntimeError):
    pass

class AuthorizationError(RuntimeError):
    pass

class AccountPrivate(RuntimeError):
    pass


class NoPostsError(RuntimeError):
    pass