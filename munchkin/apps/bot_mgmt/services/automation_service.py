import json

import requests

from munchkin.components.automation import SALT_API_URL, SALT_API_USERNAME, SALT_API_PASSWORD


class AutomationService:
    def __init__(self):

        try:
            self.headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
            response = requests.post(f"{SALT_API_URL}/login", headers=self.headers, json={
                'username': SALT_API_USERNAME,
                'password': SALT_API_PASSWORD,
                'eauth': 'pam',
            })
            response.raise_for_status()
        except Exception as err:
            raise ValueError(f"SaltAPI认证失败: {err}")

        result = response.json()
        token = result['return'][0]['token']
        self.headers['X-Auth-Token'] = token

    def __execute(self, url, client, func, tgt, args):
        data = {"client": client, 'fun': func, 'tgt': tgt}
        if args:
            data['arg'] = args
        response = requests.post(url, headers=self.headers, data=json.dumps(data), verify=False)
        response.raise_for_status()
        result = response.json()
        return result

    def execute_salt_local(self, func, tgt, args=None):
        return self.__execute(SALT_API_URL, 'local', func, tgt, args)

    def execute_salt_local_async(self, func, tgt, args=None):
        return self.__execute(SALT_API_URL, 'local_async', func, tgt, args)

    def execute_salt_find_job(self, jid):
        response = requests.get(f'{SALT_API_URL}/jobs/{jid}', headers=self.headers, verify=False)
        response.raise_for_status()
        return response.json()

    def execute_salt_ssh(self, func, tgt, args=None):
        return self.__execute(SALT_API_URL, 'ssh', func, tgt, args)

    def execute_salt_runner(self, func, tgt, args=None):
        return self.__execute(SALT_API_URL, 'runner', func, tgt, args)

    def execute_salt_wheel(self, func, tgt, args=None):
        return self.__execute(SALT_API_URL, 'wheel', func, tgt, args)
