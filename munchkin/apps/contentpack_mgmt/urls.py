from apps.contentpack_mgmt.views import ModelDownloadView, ModelUploadView, RasaModelViewSet, TrainDataDownloadView
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"api/contentpack/rasa_model", RasaModelViewSet, basename="rasa_model")
urlpatterns = router.urls

urlpatterns += [
    path(
        r"api/contentpack/model_download",
        ModelDownloadView.as_view(),
        name="model_download",
    ),
    path(
        r"api/contentpack/train_data_download",
        TrainDataDownloadView.as_view(),
        name="train_data_download",
    ),
    path(r"api/contentpack/model_upload", ModelUploadView.as_view(), name="model_upload"),
]
