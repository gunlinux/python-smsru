[![Code Health](https://landscape.io/github/gunlinux/python-smsru/master/landscape.svg?style=flat)](https://landscape.io/github/gunlinux/python-smsru/master)
[![Build Status](https://travis-ci.org/gunlinux/python-smsru.svg?branch=master)](https://travis-ci.org/gunlinux/python-smsru)

# python-smsru

A Python library for accessing the sms.ru API (http://sms.ru/?panel=api).

Based on https://github.com/umonkey/smsru-client

## Versioning and API stability

Library coverage not all of sms.ru API.

## Usage
pip install requests

### Example

    import smsru

    api = smsru.SmsClient(api_id,login,password,sender)

	print api.send('71111111111',u'test sms',test=True)

	print api.balance()

	print api.limit()

	print api.token()

	print api.cost('71111111111','test sms')

	print api.status('000000-0000000')


## Contributing

	python setup.py test

If you want to contribute, follow the [pep8](http://www.python.org/dev/peps/pep-0008/) guideline.

