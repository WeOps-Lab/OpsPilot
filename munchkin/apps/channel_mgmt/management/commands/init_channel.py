from apps.channel_mgmt.models import CHANNEL_CHOICES, Channel, ChannelUserGroup
from django.core.management import BaseCommand
from loguru import logger


class Command(BaseCommand):
    help = "初始化消息通道"

    def handle(self, *args, **options):
        logger.info("初始化企业微信应用通道")
        obj, created = Channel.objects.get_or_create(
            name=CHANNEL_CHOICES.ENTERPRISE_WECHAT.value,
            channel_type=CHANNEL_CHOICES.ENTERPRISE_WECHAT,
        )
        if created:
            obj.channel_config = {
                "channels.enterprise_wechat_channel.EnterpriseWechatChannel": {
                    "corp_id": "",
                    "secret": "",
                    "token": "",
                    "aes_key": "",
                    "agent_id": "",
                }
            }
            obj.save()
        ChannelUserGroup.objects.get_or_create(channel=obj, name="默认用户组")

        logger.info("初始化企业微信机器人通道")
        obj, created = Channel.objects.get_or_create(
            name=CHANNEL_CHOICES.ENTERPRISE_WECHAT_BOT.value,
            channel_type=CHANNEL_CHOICES.ENTERPRISE_WECHAT_BOT,
        )
        if created:
            obj.channel_config = {
                "channels.enterprise_wechat_bot_channel.EnterpriseWechatBotChannel": {
                    "enterprise_bot_url": "",
                    "secret_token": "",
                    "enable_eventbus": False,
                }
            }
            obj.save()
        ChannelUserGroup.objects.get_or_create(channel=obj, name="默认用户组")

        logger.info("初始化钉钉通道")
        obj, created = Channel.objects.get_or_create(
            name=CHANNEL_CHOICES.DING_TALK.value, channel_type=CHANNEL_CHOICES.DING_TALK
        )
        if created:
            obj.channel_config = {
                "channels.dingtalk_channel.DingTalkChannel": {
                    "client_id": "",
                    "client_secret": "",
                    "enable_eventbus": False,
                }
            }
            obj.save()
        ChannelUserGroup.objects.get_or_create(channel=obj, name="默认用户组")

        logger.info("初始化Web通道")
        obj, created = Channel.objects.get_or_create(
            name=CHANNEL_CHOICES.WEB.value,
            channel_type=CHANNEL_CHOICES.WEB,
            channel_config={"rest": {}},
        )
        ChannelUserGroup.objects.get_or_create(channel=obj, name="默认用户组")

        logger.info("初始化Gitlab通道")
        obj, created = Channel.objects.get_or_create(
            name=CHANNEL_CHOICES.GITLAB.value, channel_type=CHANNEL_CHOICES.GITLAB
        )
        if created:
            obj.channel_config = {
                "channels.gitlab_review_channel.GitlabReviewChannel": {
                    "token": "",
                    "gitlab_token": "",
                    "gitlab_url": "",
                    "secret_token": "",
                }
            }
            obj.save()
        ChannelUserGroup.objects.get_or_create(channel=obj, name="默认用户组")
