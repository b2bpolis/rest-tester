#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import locale
import re
import codecs

import json
import base64
import hashlib

import time
import datetime

import urllib
import urllib2


SIGN_TEMPLATE = '%(username)s-%(time)d-%(secret)s'
SIGNATURE_METHOD = hashlib.md5


parser = argparse.ArgumentParser(description='Cmios REST API tester')

parser.add_argument('-e', '--email', default='e@mail.ru',
                    help='user email')

parser.add_argument('-s', '--secret', default='SecRet',
                    help='authorization secret')

parser.add_argument('-H', '--host', default='casco.cmios.ru',
                    help='host')

parser.add_argument('-p', '--prefix', default='rest/default',
                    help='api url prefix')

parser.add_argument('-m', '--method', default='GET',
                    choices=('GET', 'POST', 'PUT'),
                    help='request method')

parser.add_argument('-j', '--json', help='json file')

parser.add_argument('url', help='api url')



def sign(username, time, secret):
    string = SIGN_TEMPLATE % dict(username=username, time=time, secret=secret)
    return SIGNATURE_METHOD(string).hexdigest()

def get_token(username, secret):
    now = int(time.mktime(datetime.datetime.now().timetuple()))
    signature = sign(username, now, secret)
    params = dict(
        username=username,
        time=now,
        signature=signature
    )
    token = base64.urlsafe_b64encode(urllib.urlencode(params))
    return token

def create_url(args):
    host = args.host
    if not re.match(r'^https?://', host):
        host = 'http://%s' % host
    if host.endswith('/'):
        host = host[:-1]

    prefix = args.prefix
    if not re.search(r'/', prefix):
        prefix = 'rest/%s' % prefix

    url = args.url
    if not url.endswith('/'):
        url = '%s/' % url


    return '%s/%s/%s' % (host, prefix, url)

def pprint(str):
    print json.dumps(json.loads(str), sort_keys=True, indent=4
        ).decode('unicode-escape').encode(locale.getpreferredencoding())


args = parser.parse_args()

token = get_token(args.email, args.secret)

url = create_url(args)

headers = {
    'X-Authorization': token,
    'User-Agent': 'casco rest tester',
    'Content-Type': 'application/json',
}

method = args.method

data = None

if args.json:
    data = codecs.open(args.json, 'r', 'utf8').read()

if method == 'POST' and data is None:
    data = '{}'

request = urllib2.Request(url, data=data, headers=headers)
request.get_method = lambda: method

try:
    response = urllib2.urlopen(request)
except urllib2.HTTPError, e:
    print e

    body = e.read()
    try:
        pprint(body)
    except ValueError:
        print body
else:
    pprint(response.read())
