#sms lib for sms.ru api
based on https://github.com/umonkey/smsru-client	



s = SmsClient(api_id,login,password,sender)

print s.send('71111111111',u'test sms',test=True)

print s.balance()

print s.limit()

print s.token()

print s.cost('71111111111','test sms')

print s.status('000000-0000000')
