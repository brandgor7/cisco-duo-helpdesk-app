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
import time
from pprint import pprint


class DuoAuthenticator:
    def __init__(self):
        # Access environment variables
        # For both Auth and Admin Duo API
        self.auth_ikey = config.DUO_IKEY
        self.auth_skey = config.DUO_SKEY
        self.auth_api_url = config.DUO_API_URL
        self.auth_host = self.parse_hostname(self.auth_api_url)
        self.admin_ikey = config.DUO_ADMIN_IKEY
        self.admin_skey = config.DUO_ADMIN_SKEY
        self.admin_api_url = config.DUO_ADMIN_API_URL
        self.admin_host = self.parse_hostname(self.admin_api_url)

    def parse_hostname(self, url):
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        if not host:
            print("Error: Unable to parse hostname from API_URL.")
            sys.exit(1)
        return host

    def generate_headers(self, method, path, params):
        if path.startswith('/admin'):
            ikey = self.admin_ikey
            skey = self.admin_skey
            host = self.admin_host
        else:
            ikey = self.auth_ikey
            skey = self.auth_skey
            host = self.auth_host
        now = email.utils.formatdate()
        canon = [now, method.upper(), host.lower(), path]
        args = []
        for key in sorted(params.keys()):
            val = params[key].encode("utf-8")
            args.append(
                '%s=%s' % (urllib.parse.quote(key, '~'), urllib.parse.quote(val, '~')))
        canon.append('&'.join(args))
        canon = '\n'.join(canon)
        sig = hmac.new(bytes(skey, encoding='utf-8'),
                       bytes(canon, encoding='utf-8'), hashlib.sha1)
        auth = '%s:%s' % (ikey, sig.hexdigest())
        return ('&'.join(args), {
            'Date': now,
            'Authorization': 'Basic %s' % base64.b64encode(bytes(auth, encoding="utf-8")).decode(),
            'Content-Type': 'application/x-www-form-urlencoded'
        })

    def authenticate_user(self, payload):
        user_email = payload.get("email", "")
        username = payload.get("username", "")
        device = "auto"  # or extract from payload's devices array if needed

        uri = '/auth/v2/auth'
        params = {'username': username, 'factor': 'push', 'device': device, 'async': '1'}
        body, headers = self.generate_headers('POST', uri, params)

        # Use self.auth_host instead of self.host
        response = requests.post(f'https://{self.auth_host}{uri}', headers=headers, data=body).json()

        if response['stat'] != 'OK':
            return response
        return self.check_auth_status(response['response']['txid'])

    def check_auth_status(self, txid, timeout=60, interval=5):
        uri = '/auth/v2/auth_status'
        params = {'txid': txid}
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                return "Error: Timeout"
            args, headers = self.generate_headers('GET', uri, params)
            result = requests.get(f'https://{self.auth_host}{uri}?{args}', headers=headers).json()
            if result['stat'] != 'OK':
                return result
            if result['response']['result'] in ['allow', 'deny']:
                return result['response']['result']
            time.sleep(interval)

    def fetch_users(self):
        uri = '/admin/v1/users'
        params_f = '?limit={}&offset={}'
        result = []
        more = True
        limit = '100'
        offset = '0'
        while more:
            params = params_f.format(limit, offset)
            body, headers = self.generate_headers('GET', uri, {'limit': limit, 'offset': offset})
            response = requests.get(f'https://{self.admin_host}{uri}{params}', headers=headers).json()
            if response['stat'] != 'OK':
                return response
            for user in response['response']:
                if user['status'] != 'active' and user['status'] != 'bypass':
                    continue
                user_dict = {
                    'username': user['username'],
                    'fullname': user['realname'],
                    'email': user['email'],
                    'status': user['status'],
                }
                devices = []
                for phone in user['phones']:
                    if phone['activated']:
                        try:
                            phone['capabilities'].remove('auto')
                        except ValueError:
                            pass
                        devices.append({
                            'id': phone['phone_id'],
                            'type': 'phone',
                            'capabilities': phone['capabilities'],
                            'model': phone['model'],
                            'number': phone['number']
                        })
                user_dict['devices'] = devices
                result.append(user_dict)
            if response['metadata'].get('next_offset'):
                pprint(response['metadata'])
                offset = str(response['metadata'].get('next_offset'))
            else:
                pprint(response['metadata'])
                more = False
        return result


# Instantiate the DuoAuthenticator
duo_authenticator = DuoAuthenticator()
