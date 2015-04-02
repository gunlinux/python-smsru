"""
    Custom Exception
"""


class SmsruError(Exception):

    """2Gis API error"""

    def __init__(self, code, message):
        Exception.__init__(self)
        self.code = code
        self.message = message

    def __str__(self):
        return self.message
