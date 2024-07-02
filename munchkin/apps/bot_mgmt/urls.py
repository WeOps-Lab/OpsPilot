from apps.bot_mgmt.serializers.model_download_view import ModelDownloadView
from apps.bot_mgmt.serializers.rasa_model_view import RasaModelViewSet
from apps.bot_mgmt.views import BotViewSet, SkillExecuteView, SaltExecuteView
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"api/bot", BotViewSet)
router.register(r"api/rasa_model", RasaModelViewSet, basename="rasa_model")
urlpatterns = router.urls

urlpatterns += [
    path(r"api/bot/skill_execute", SkillExecuteView.as_view(), name="skill_execute"),
    path(r'api/bot/salt_execute', SaltExecuteView.as_view(), name='salt_execute'),
    path(
        r"api/rasa_model/model_download",
        ModelDownloadView.as_view(),
        name="model_download",
    ),
]
