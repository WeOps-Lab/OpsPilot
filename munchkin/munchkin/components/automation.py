import os

SALT_API_URL = os.getenv('SALT_API_URL', 'http://saltstack-server.ops-pilot:8000')
SALT_API_USERNAME = os.getenv('SALT_API_USERNAME', 'saltapi')
SALT_API_PASSWORD = os.getenv('SALT_API_PASSWORD', 'password')