from django.urls import path
from rest_framework import routers

from apps.knowledge_mgmt.views import RagSearchView

router = routers.DefaultRouter()
urlpatterns = router.urls
urlpatterns += [
    path(r'api/rag_search', RagSearchView.as_view(), name='rag_search'),
]
