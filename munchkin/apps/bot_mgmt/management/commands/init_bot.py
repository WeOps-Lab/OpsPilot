from django.core.management import BaseCommand

from apps.bot_mgmt.models import Bot
from apps.channel_mgmt.models import Channel, CHANNEL_CHOICES
from apps.contentpack_mgmt.models import RasaModel


class Command(BaseCommand):
    help = '初始化机器人'

    def handle(self, *args, **options):
        Channel.objects.filter(channel_type=CHANNEL_CHOICES.WEB).first()
        rasa_model = RasaModel.objects.filter(name='核心模型').first()
        ops_pilot = Bot.objects.create(name='OpsPilot', description='智能运维助理',
                                       assistant_id='ops_pilot',
                                       rasa_model=rasa_model)
        ops_pilot.channels.add(Channel.objects.get(channel_type=CHANNEL_CHOICES.WEB))
        ops_pilot.save()
