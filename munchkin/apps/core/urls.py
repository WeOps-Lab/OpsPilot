from apps.core.views.user_view import UserView
from django.conf.global_settings import INSTALLED_APPS
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

admin.site.site_title = "Munchkin 管理后台"
admin.site.site_header = admin.site.site_title
public_router = routers.DefaultRouter()
public_router.register(r"api/public/user_view", UserView, basename="user_view")

urlpatterns = public_router.urls

urlpatterns += [
    path("select2/", include("django_select2.urls")),
]


def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)

    app_count = len(INSTALLED_APPS)  # 获取app数量

    app_list = sorted(
        app_dict.values(),
        key=lambda x: INSTALLED_APPS.index(x["app_label"]) if x["app_label"] in INSTALLED_APPS else app_count,
    )
    # 如果应用标签(如app1, app2, 在INSTALLED_APPS中，则按其索引排，
    # 否则排最后面
    app_list = list(reversed(app_list))
    for app in app_list:
        app["models"].sort(key=lambda x: x["name"])

    return app_list


admin.AdminSite.get_app_list = get_app_list
