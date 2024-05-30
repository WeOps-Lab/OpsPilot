from django.contrib import admin
from rest_framework import routers
from django.urls import path, include

from apps.core.views.postgrest_view import PostgrestAPIView
from apps.core.views.user_view import UserView

admin.site.site_title = "Munchkin 管理后台"
admin.site.site_header = admin.site.site_title
public_router = routers.DefaultRouter()
public_router.register(r"api/public/user_view", UserView, basename="user_view")

urlpatterns = public_router.urls

urlpatterns += [
    path('api/pgr/', include([
        path('<path:path>', PostgrestAPIView.as_view()),
    ])),
]
