# -*- coding: utf-8 -*-

"""
python-smsru
============

A Python library for accessing the sms.ru API
"""

from setuptools import setup, find_packages


setup(
    name='smsru',
    version='0.0.2',
    author='gunlinux',
    author_email='gunlinux@ya.ru',
    url='https://github.com/gunlinux/python-smsru',
    description='sms.ru api library for Python',
    long_description=__doc__,
    license='GPL',
    packages=find_packages(),
    test_suite='tests',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
    ),
    install_requires=[
        'requests',
        ]
)
