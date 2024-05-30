import json

from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask


class CeleryUtils:
    @staticmethod
    def create_or_update_periodic_task(name, crontab=None, interval=None, task=None, args=None, kwargs=None,
                                       enabled=True):
        """
        创建或更新周期任务
        :param name: 任务名称
        :param crontab: crontab表达式，如：'0 0 * * *'，默认为None
        :param interval: 间隔时间，如：60（秒），默认为None
        :param task: 任务函数，如：'app.tasks.send_email'，默认为None
        :param args: 任务函数的位置参数，如：(1, 2, 3)，默认为None
        :param kwargs: 任务函数的关键字参数，如：{'to': 'example@example.com', 'subject': 'Hello'}，默认为None
        :param enabled: 是否启用该任务，默认为True
        """
        if crontab:
            minute, hour, day_of_month, month_of_year, day_of_week = crontab.split()
            kwargs = dict(
                minute=minute,
                hour=hour,
                day_of_month=day_of_month,
                month_of_year=month_of_year,
                day_of_week=day_of_week,
            )
            schedule, _ = CrontabSchedule.objects.get_or_create(**kwargs, defaults=kwargs)
        elif interval:
            kwargs = dict(every=interval, period='seconds')
            schedule, _ = IntervalSchedule.objects.get_or_create(**kwargs, defaults=kwargs)
        else:
            raise ValueError('Either crontab or interval must be provided')

        defaults = dict(
            name=name,
            task=task,
            args=json.dumps(args) if args else '[]',
            kwargs=json.dumps(kwargs) if kwargs else '{}',
            enabled=enabled,
            schedule=schedule,
        )
        PeriodicTask.objects.update_or_create(name=name, defaults=defaults)

    @staticmethod
    def delete_periodic_task(name):
        """
        删除周期任务
        :param name: 任务名称
        """
        PeriodicTask.objects.filter(name=name).delete()

    @staticmethod
    def get_periodic_task(name):
        """
        获取周期任务
        :param name: 任务名称
        :return: 任务对象，如果不存在则返回None
        """
        try:
            return PeriodicTask.objects.get(name=name)
        except PeriodicTask.DoesNotExist:
            return None

    @staticmethod
    def get_all_periodic_tasks():
        """
        获取所有周期任务
        :return: 所有周期任务的查询集
        """
        return PeriodicTask.objects.all()

    @staticmethod
    def enable_periodic_task(name):
        """
        启用周期任务
        :param name: 任务名称
        """
        task = CeleryUtils.get_periodic_task(name)
        if task:
            task.enabled = True
            task.save()

    @staticmethod
    def disable_periodic_task(name):
        """
        禁用周期任务
        :param name: 任务名称
        """
        task = CeleryUtils.get_periodic_task(name)
        if task:
            task.enabled = False
            task.save()
