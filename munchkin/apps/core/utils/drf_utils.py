from rest_framework.pagination import PageNumberPagination
from apps.core.utils.web_utils import WebUtils


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 10000

    def paginate_queryset(self, queryset, request, view=None):
        # 统一page格式
        page_size = request.GET.get("page_size", "10")
        if page_size == "-1":
            return None
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        # 统一response格式
        return WebUtils.response_success(dict(count=self.page.paginator.count, data=data))
