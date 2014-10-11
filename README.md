# python-smsru

A Python library for accessing the sms.ru API (http://sms.ru/?panel=api).

Based on https://github.com/umonkey/smsru-client

## Versioning and API stability

API stability isn't guaranteed before **1.3** version. Library version always will match sms.ru API version.

Library coverage 50% of sms.ru API.

## Usage

### Example

    import smsru

    client = smsru.SmsClient(api_id,login,password,sender)

	print s.send('71111111111',u'test sms',test=True)

	print s.balance()

	print s.limit()

	print s.token()

	print s.cost('71111111111','test sms')

	print s.status('000000-0000000')

## Contributing

If you want to contribute, follow the [pep8](http://www.python.org/dev/peps/pep-0008/) guideline.

