[![Code Health](https://landscape.io/github/gunlinux/python-smsru/master/landscape.svg?style=flat)](https://landscape.io/github/gunlinux/python-smsru/master)
[![Build Status](https://travis-ci.org/gunlinux/python-smsru.svg?branch=master)](https://travis-ci.org/gunlinux/python-smsru)

# python-smsru

A Python library for accessing the sms.ru API (http://sms.ru/?panel=api).

Based on https://github.com/umonkey/smsru-client

## Versioning and API stability

Library coverage not all of sms.ru API.

## Dependencies
This package is requires ```requests``` package. Dependencies should be installed automatically by pip.

## Installation
pip install smsru

## Usage

First of all you need to import this library:
```python
import smsru
```

In version 0.0 you can use limited group of API methods:
```python
sms_api = smsru.SmsClient(api_id, login, password, sender)

print sms_api.send("+71234567890", u'sms text', test=True)
```
and so on with balance/limit/token/cost/status methods.

In current version you can use all API methods, but the usage is little bit different:
Now you need to get api-object that is a chain between you and sms.ru:
```python
sms_client = smsru.SmsClient(api_id)
sms_api = sms_client.get_api()
```
You also can see, that only api_id parameter is now required, because it's enough to authorize

When you got your api-object, you can get access to any sms.ru API this way:
```python
sms_api.sms.send(to='+71234567890', text='Hello message.')
#or
sms_api.my.limit()
```
The structure of api-object is automatically generated to correspond the sms.ru API structure.
For example to call /sms/\* methods, you can use methods of 'sms' api-object member.
As you can see, api_id parameter(required by all API-methods) is substituted automatically.
Other parameters are substituted to API-request with names you give them in methods call.

### Example

    import smsru

    client = smsru.SmsClient(api_id,login,password,sender)
    api = client.get_api()
    sms_id = api.sms.send(to='+71234567890', text=u'Текст сообщения', translit=1)[1]
    print(api.sms.status(sms_id))
    print(api.my.balance())

## Contributing

Please run tests before any pull-requests:
```bash
	python setup.py test
```

If you want to contribute, follow the [pep8](http://www.python.org/dev/peps/pep-0008/) guideline.

