import wrapt
from rest_framework import status

from apps.core.constants import AUTH_TOKEN_HEADER_NAME
from apps.core.utils.keycloak_client import KeyCloakClient
from apps.core.utils.web_utils import WebUtils


def uma_permission(permission: str):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        token: str = args[0].META.get(AUTH_TOKEN_HEADER_NAME)
        if token is None:
            return WebUtils.response_error(error_message='用户Token缺失', status=status.HTTP_403_FORBIDDEN)

        client = KeyCloakClient()

        if client.is_super_admin(token):
            return wrapped(*args, **kwargs)

        if client.has_permission(token, permission):
            return wrapped(*args, **kwargs)
        else:
            return WebUtils.response_error(error_message='用户无此权限', status=status.HTTP_403_FORBIDDEN)

    return wrapper
