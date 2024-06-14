AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # this is default
    "apps.core.middlewares.bk_token.backends.TokenBackend",  # 蓝鲸token_backend
    "guardian.backends.ObjectPermissionBackend",
)
