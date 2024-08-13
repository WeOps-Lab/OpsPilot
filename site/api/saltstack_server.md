SaltStack Server is used to provide automation capabilities for OpsPilot

## SaltStack Server

### example

```python
import json
import requests

SALT_API_URL = "http://saltstack-server.ops-pilot"
SALT_API_USERNAME = "saltapi"
SALT_API_PASSWORD = "password"


def get_token():
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {
        'username': SALT_API_USERNAME,
        'password': SALT_API_PASSWORD,
        'eauth': 'pam',
    }
    response = requests.post(f"{SALT_API_URL}/login", headers=headers, json=data)
    response.raise_for_status()
    return response.json()['return'][0]['token']


def execute_salt_command(client, func, tgt, args=None):
    token = get_token()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Auth-Token': token,
    }
    data = {"client": client, 'fun': func, 'tgt': tgt}
    if args:
        data['arg'] = args
    response = requests.post(SALT_API_URL, headers=headers, json=data, verify=False)
    response.raise_for_status()
    return response.json()


def execute_local(func, tgt, args=None):
    return execute_salt_command('local', func, tgt, args)


def execute_local_async(func, tgt, args=None):
    return execute_salt_command('local_async', func, tgt, args)


def find_job(jid):
    token = get_token()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Auth-Token': token,
    }
    response = requests.get(f'{SALT_API_URL}/jobs/{jid}', headers=headers, verify=False)
    response.raise_for_status()
    return response.json()


def execute_ssh(func, tgt, args=None):
    return execute_salt_command('ssh', func, tgt, args)


def execute_runner(func, tgt, args=None):
    return execute_salt_command('runner', func, tgt, args)


def execute_wheel(func, tgt, args=None):
    return execute_salt_command('wheel', func, tgt, args)


# 示例调用
if __name__ == "__main__":
    response = execute_ssh('test.ping', '127.0.0.1')
    print(json.dumps(response, indent=4))

```