from django.urls import path
from rest_framework import routers

from apps.knowledge_mgmt.views import KnowledgeView

router = routers.DefaultRouter()
urlpatterns = router.urls
urlpatterns += [
    path(r'api/knowledge/search', KnowledgeView.as_view(), name='knowledge'),
]
