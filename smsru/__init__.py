""" http://sms.ru/?panel=api. """

import time
import hashlib
import requests
from .exceptions import SmsruError

__version__ = '0.0.2'

SEND_STATUS = {
    100: "Message accepted",
    201: "Out of money",
    202: "Bad recipient",
    203: "Message text not specified",
    204: "Bad sender (unapproved)",
    205: "Message too long",
    206: "Day message limit reached",
    207: "Can't send messages to that number",
    208: "Wrong time",
    209: "Blacklisted recipient",
}

STATUS_STATUS = {
    -1: "Message not found",
    100: "Message is in the queue",
    101: "Message is on the way to the operator",
    102: "Message is on the way to the recipient",
    103: "Message delivered",
    104: "Message failed: out of time",
    105: "Message failed: cancelled by the operator",
    106: "Message failed: phone malfunction",
    107: "Message failed, reason unknown",
    108: "Message declined",
}

COST_STATUS = {
    100: "Success"
}


class SmsClient(object):

    """sms.ru API."""

    def __init__(self, api_id, login=None, password=None, sender=None):
        """

        Init of api.

        Parameters::
            api_id : API key
            login : user login
            password : user password
            sender : user default sender
        """
        self.api_id = api_id
        self._password = password
        self.login = login
        self._token = None
        self.sender = sender
        self._token_ts = 0

    def get_api(self):
        return SmsApiMethod(self)

    @classmethod
    def token(cls):
        """Return a token."""
        url = "http://sms.ru/auth/get_token"
        res = requests.get(url).text.strip().split("\n")
        return res[0]

    def _get_sign(self):
        """ helper for token auth """
        return hashlib.md5(self._password.encode('utf-8') + self._token.encode('utf-8')).hexdigest()

    def call(self, method, args=None):
        """ Main helper """

        if args:
            args = args.copy()
        else:
            args = {}

        args["api_id"] = self.api_id
        if method in ("sms/send", "sms/cost", 'sms/balance') and self.api_id is None:
            args['login'] = self.login
            args['token'] = self._get_token()
            args['sig'] = self._get_sign()
            del args["api_id"]
        if self.sender:
            args['from'] = self.sender

        url = "http://sms.ru/%s" % method

        res = requests.get(url, params=args).text.split("\n")
        if res[0] == "200":
            raise SmsruError(200, "The supplied API key is wrong")
        elif res[0] == "210":
            raise SmsruError(210, "GET used when POST must have been")
        elif res[0] == "211":
            raise SmsruError(211, "Unknown method")
        elif res[0] == "220":
            raise SmsruError(220, "The service is temporarily unavailable")
        elif res[0] == "301":
            raise SmsruError(301, "Wrong password")
        return res

    def _get_token(self):
        """Return a token.  Refreshes it if necessary."""
        if self._token_ts < time.time() - 500:
            self._token = None
        if self._token is None:
            self._token = self.token()
            self._token_ts = time.time()
        return self._token

    def send(self, number, text, test=None):
        """ http://sms.ru/?panel=api&subpanel=method&show=sms/send """
        if test is None:
            return self.call('sms/send', {'to': number, 'text': text})
        return self.call('sms/send', {'to': number, 'text': text, 'test': 1})

    def balance(self):
        """ http://sms.ru/?panel=api&subpanel=method&show=my/balance """
        return self.call('my/balance')

    def limit(self):
        """ http://sms.ru/?panel=api&subpanel=method&show=my/limit """
        return self.call('my/limit')

    def status(self, msgid):
        """
            Return message status.

            http://sms.ru/?panel=api&subpanel=method&show=sms/status
        """
        res = self.call('my/balance', {"id": msgid})
        code = int(res[0])
        text = STATUS_STATUS.get(code, "Unknown status")
        return [res[0], text]

    def cost(self, number, message):
        """
            Prints the cost of the message.

            http://sms.ru/?panel=api&subpanel=method&show=sms/cost
        """
        res = self.call(
            'sms/cost', {"to": number, "text": message.encode("utf-8")})
        if res[0] != "100":
            res.extend([None, None])
        return [res[0], COST_STATUS.get(int(res[0]), "Unknown status"),
                res[1], res[2]]

class SmsApiMethod:
    def __init__(self, api, method=None):
        self._api = api
        self._method = method

    def __getattr__(self, method):
        if self._method:
            self._method += '/' + method
            return self

        return SmsApiMethod(self._api, method)

    def __call__(self, *args, **kwargs):
        return self._api.call(self._method, kwargs)

