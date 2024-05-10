import json

import requests

from actions.constants.server_settings import server_settings


class AutomationService:
    def __init__(self):

        try:
            self.headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
            response = requests.post(f"{server_settings.salt_api_url}/login", headers=self.headers, json={
                'username': server_settings.salt_api_username,
                'password': server_settings.salt_api_password,
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
        return self.__execute(server_settings.salt_api_url, 'local', func, tgt, args)

    def execute_salt_local_async(self, func, tgt, args=None):
        return self.__execute(server_settings.salt_api_url, 'local_async', func, tgt, args)

    def execute_salt_find_job(self, jid):
        response = requests.get(f'{server_settings.salt_api_url}/jobs/{jid}', headers=self.headers, verify=False)
        response.raise_for_status()
        return response.json()

    def execute_salt_ssh(self, func, tgt, args=None):
        return self.__execute(server_settings.salt_api_url, 'ssh', func, tgt, args)

    def execute_salt_runner(self, func, tgt, args=None):
        return self.__execute(server_settings.salt_api_url, 'runner', func, tgt, args)

    def execute_salt_wheel(self, func, tgt, args=None):
        return self.__execute(server_settings.salt_api_url, 'wheel', func, tgt, args)
