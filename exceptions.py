'''
Master of all exceptions, errors
'''

class InvalidArgumentError(ValueError):
    pass

class OperationFailedException(Exception):
    pass

class NotImplementedException(Exception):
    pass