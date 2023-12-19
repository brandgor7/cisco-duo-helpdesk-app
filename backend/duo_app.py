"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at https://developer.cisco.com/docs/licenses.
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import sys
import base64
import email.utils
import hmac
import hashlib
import urllib.parse
import requests
from urllib.parse import urlparse
from config.config import config

# Access environment variables
IKEY = config.DUO_IKEY
SKEY = config.DUO_SKEY
API_URL = config.DUO_API_URL


class DuoAuthenticator:
    def __init__(self, ikey, skey, api_url):
        self.ikey = ikey
        self.skey = skey
        self.api_url = api_url
        self.host = self.parse_hostname(api_url)

    def parse_hostname(self, url):
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        if not host:
            print("Error: Unable to parse hostname from API_URL.")
            sys.exit(1)
        return host

    def generate_headers(self, method, path, params):
        now = email.utils.formatdate()
        canon = [now, method.upper(), self.host.lower(), path]
        args = []
        for key in sorted(params.keys()):
            val = params[key].encode("utf-8")
            args.append(
                '%s=%s' % (urllib.parse.quote(key, '~'), urllib.parse.quote(val, '~')))
        canon.append('&'.join(args))
        canon = '\n'.join(canon)
        sig = hmac.new(bytes(self.skey, encoding='utf-8'),
                       bytes(canon, encoding='utf-8'), hashlib.sha1)
        auth = '%s:%s' % (self.ikey, sig.hexdigest())
        return ('&'.join(args), {
            'Date': now,
            'Authorization': 'Basic %s' % base64.b64encode(bytes(auth, encoding="utf-8")).decode(),
            'Content-Type': 'application/x-www-form-urlencoded'
        })

    def authenticate_user(self, user_email):
        uri = '/auth/v2/auth'
        params = {'username': user_email, 'factor': 'push', 'device': 'auto', 'async': '1'}
        body, headers = self.generate_headers('POST', uri, params)
        response = requests.post(f'https://{self.host}{uri}', headers=headers, data=body).json()
        if response['stat'] != 'OK':
            return response
        return self.check_auth_status(response['response']['txid'])

    def check_auth_status(self, txid, timeout=60, interval=5):
        import time
        uri = '/auth/v2/auth_status'
        params = {'txid': txid}
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                return "Error: Timeout"
            args, headers = self.generate_headers('GET', uri, params)
            result = requests.get(f'https://{self.host}{uri}?{args}', headers=headers).json()
            if result['stat'] != 'OK':
                return result
            if result['response']['result'] in ['allow', 'deny']:
                return result['response']['result']
            time.sleep(interval)


# Instantiate the DuoAuthenticator
duo_authenticator = DuoAuthenticator(IKEY, SKEY, API_URL)
