import os

from django.conf import settings

from celery.schedules import crontab

if os.getenv("ENABLE_CELERY", "False").lower() == "true":
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    DJANGO_CELERY_BEAT_TZ_AWARE = False
    CELERY_ENABLE_UTC = False
    CELERY_WORKER_CONCURRENCY = 2  # 并发数
    CELERY_MAX_TASKS_PER_CHILD = 5  # worker最多执行5个任务便自我销毁释放内存
    CELERY_TIMEZONE = settings.TIME_ZONE  # celery 时区问题
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    CELERY_BEAT_SCHEDULER = os.getenv("CELERY_BEAT_SCHEDULER")  # Backend数据库
    CELERY_IMPORTS = ("apps.core.tasks", "apps.knowledge_mgmt")
    CELERY_BEAT_SCHEDULE = {
        "auditlog_flush_task": {
            "task": "munchkin.app.core.tasks.auditlog_flush_task",
            "schedule": crontab(minute=0, hour=0),
        },
    }
