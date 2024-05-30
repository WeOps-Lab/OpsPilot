from datetime import timedelta

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",  # 日期时间格式配置
    "DATE_FORMAT": "%Y-%m-%d",
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        # 'apps.core.middlewares.keycloak_permission_middleware.KeyCloakPermissionMiddleware'
        "rest_framework.permissions.IsAuthenticated",  # 只有经过身份认证确定用户身份才能访问
        # 'rest_framework.authentication.TokenAuthentication'
        # 'rest_framework.permissions.IsAdminUser', # is_staff=True才能访问 —— 管理员(员工)权限
        # "rest_framework.permissions.AllowAny",  # 允许所有
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly', # 有身份 或者 只读访问(self.list,self.retrieve)
    ],
}

SIMPLE_JWT = {
    # token有效时长
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    # token刷新后的有效时间
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # 设置前缀
    "AUTH_HEADER_TYPES": ("JWT",),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "basic": {"type": "basic"},
        "bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
    "APIS_SORTER": "alpha",
    "JSON_EDITOR": True,
    "OPERATIONS_SORTER": "alpha",
    "VALIDATOR_URL": None,
    "AUTO_SCHEMA_TYPE": 2,  # 分组根据url层级分，0、1 或 2 层
}
