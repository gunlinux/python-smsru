# encoding=utf-8
import hashlib
import os
import time
import urllib
import urllib2

from conf import api_id,password,login,sender


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

class NotConfigured(Exception):
    pass


class WrongKey(Exception):
    pass


class InternalError(Exception):
    pass


class Unavailable(Exception):
    pass


class SmsClient(object):
    def _get_sign(self):
        return  hashlib.md5(self._password +self._token).hexdigest()
    def __init__(self,api_id,login,password,sender=''):
        self.api_id = api_id
        self._password = password
        self.login  = login
        self._token = None
        self.sender = sender
        self._token_ts = 0

    def _call(self, method, args={}):
        args["api_id"] = self.api_id
        if method in ("sms/send", "sms/cost",'sms/balance'):
            args['login']=self.login
            args['token']= self._get_token()
            args['sig'] = self._get_sign()
            del args["api_id"]
        if self.sender<>'':
            args['from'] = self.sender
        url = "http://sms.ru/%s?%s" % (method, urllib.urlencode(args))
        res = urllib2.urlopen(url).read().strip().split("\n")
        if res[0] == "200":
            raise WrongKey("The supplied API key is wrong")
        elif res[0] == "210":
            raise InternalError("GET used when POST must have been")
        elif res[0] == "211":
            raise InternalError("Unknown method")
        elif res[0] == "220":
            raise Unavailable("The service is temporarily unavailable")
        elif res[0] == "301":
            raise NotConfigured("Wrong password")
        return res

    def send(self,to,text,test=False):
        return self._call('sms/send',{'to':to,'text':text,'test':test})

    def balance(self):
        return self._call('my/balance')

    def limit(self):
        return self._call('my/limit')

    def _get_token(self):
        """Returns a token.  Refreshes it if necessary."""
        if self._token_ts < time.time() - 500:
            self._token = None
        if self._token is None:
            self._token = self.token()
            self._token_ts = time.time()
        return self._token
  
    def token(self):
        """Returns a token."""
        url = "http://sms.ru/auth/get_token"
        res = urllib2.urlopen(url).read().strip().split("\n")
        return res[0]
  
    def status(self, msgid):
        """Returns message status."""
        res = self._call('my/balance',{"id":msgid})
        code = int(res[0])
        text = STATUS_STATUS.get(code, "Unknown status")
        return [res[0], text]

    def cost(self, to, message):
        """Prints the cost of the message."""
        res = self._call('sms/cost',{"to": to, "text": message.encode("utf-8")})
        if res[0] != "100":
            res.extend([None, None])
        return [res[0], COST_STATUS.get(int(res[0]), "Unknown status"), res[1], res[2]]

if __name__=='__main__':
	s = SmsClient(api_id,login,password,sender)
	print s.send('71111111111',u'test sms',test=True)
	print s.balance()
	print s.limit()
	print s.token()
	print s.cost('71111111111','test sms')
	print s.status('000000-0000000')
