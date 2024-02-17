class WrongDateFormat(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class WrongSwipeMonthParameterProvided(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
