# -*- coding: utf-8 -*-
"""Django project settings
"""
from actions.constant.server_settings import server_settings

# try:
#     from django.conf import settings
#
#     APP_CODE = settings.APP_ID
#     SECRET_KEY = settings.APP_TOKEN
#     COMPONENT_SYSTEM_HOST = getattr(settings, 'BK_PAAS_INNER_HOST', settings.BK_PAAS_HOST)
#     DEFAULT_BK_API_VER = getattr(settings, 'DEFAULT_BK_API_VER', 'v2')
# except Exception:
#     APP_CODE = ''
#     SECRET_KEY = ''
#     COMPONENT_SYSTEM_HOST = ''
#     DEFAULT_BK_API_VER = 'v2'


APP_CODE = server_settings.bkapp_app_code
SECRET_KEY = server_settings.bkapp_app_token
COMPONENT_SYSTEM_HOST = server_settings.bkapp_bk_paas_host
DEFAULT_BK_API_VER = server_settings.bkapp_api_ver

CLIENT_ENABLE_SIGNATURE = False
