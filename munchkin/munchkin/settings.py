from dotenv import load_dotenv
from split_settings.tools import include, optional

load_dotenv()

include(
    'components/base.py',
    'components/audit_log.py',
    'components/database.py',
    'components/rest_framework.py',
    'components/celery.py',
    optional('local_settings.py'),
)
