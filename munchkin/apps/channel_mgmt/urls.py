from rest_framework import routers

from apps.channel_mgmt.views.channel_viewset import ChannelViewSet

router = routers.DefaultRouter()
router.register(r'api/channels', ChannelViewSet)
urlpatterns = router.urls

urlpatterns += []
