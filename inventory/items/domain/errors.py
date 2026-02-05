class InvariantError(ValueError):
    pass


class DuplicateNameError(InvariantError):
    pass


class NotFoundError(KeyError):
    pass
