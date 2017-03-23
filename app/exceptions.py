class UserAlreadyExistsException(ValueError):
    pass

class JsonOutputException(ValueError):
    pass

class ValidationError(ValueError):
    pass

class FormValidateError(ValueError):
    pass

class AdminException(ValueError):
    pass