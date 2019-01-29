

class IncorrectExchangeException(Exception):
    """ When the user uploads the a file which is not supported for the
        specific exchange they want a conversion for
    """

    def __init__(self, arg1, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        super(IncorrectExchangeException, self).__init__(arg1)


class IncorrectFileFormat(Exception):
    """
    When the user provides an "other than" supported filetype
    """

    def __init__(self, arg1, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        super(IncorrectFileFormat, self).__init__(arg1)


class EmptyExchangeField(Exception):
    """
    When the user does not select and exchange
    """

    def __init__(self, arg1, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        super(EmptyExchangeField, self).__init__(arg1)


class EmptyServiceField(Exception):
    """
    When the user does not select a service
    """

    def __init__(self, arg1, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        super(EmptyServiceField, self).__init__(arg1)
