from munchkin.components.base import MIDDLEWARE

AUDITLOG_INCLUDE_ALL_MODELS = True

MIDDLEWARE += [
    'auditlog.middleware.AuditlogMiddleware',
]
