class UnexpectedDatetimeFormat(Exception):
    def __init__(self, details):
        self.details = details
