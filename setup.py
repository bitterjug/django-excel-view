#!/usr/bin/env python

from distutils.core import setup

setup(
    name='django-excel-view',
    version='1.0',
    description='''A tool for DRY spreadsheet column specifications,
and a django class-based view that depends on it to
return a simple spreadsheet using django-excel-response''',
    author='Mark Skipper',
    author_email='marks@aptivate.org',
    url='https://github.com/markskipper/django-excel-view',
    packages=['excel_view'],
    long_description=open('README.rst').read(),
    requires=['xlwt', 'django-excel-response'],
    classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Office/Business :: Financial :: Spreadsheet',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
