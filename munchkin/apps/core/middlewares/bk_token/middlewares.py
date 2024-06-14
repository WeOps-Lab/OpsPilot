# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from django.conf import settings
from django.contrib import auth
from django.core.cache import cache

from apps.core.middlewares.bk_token.forms import AuthenticationForm

try:
    from django.utils.deprecation import MiddlewareMixin
except Exception:  # pylint: disable=broad-except
    MiddlewareMixin = object


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        """
        Login paas by two ways
        1. views decorated with 'login_exempt' keyword
        2. User has logged in calling auth.login
        """

        if getattr(view, "login_exempt", False):
            return None

        if not settings.BK_PAAS_HOST:
            # 没有配置蓝鲸host地址, 不做登录校验
            return None

        # 先做数据清洗再执行逻辑
        user = self.authenticate(request)
        if user:
            return None

    def process_response(self, request, response):
        return response

    def authenticate(self, request):
        form = AuthenticationForm(request.COOKIES)
        if not form.is_valid():
            return None

        bk_token = form.cleaned_data["bk_token"]
        session_key = request.session.session_key
        if session_key:
            # 确认 cookie 中的 ticket 和 cache 中的是否一致
            cache_session = cache.get(session_key)
            is_match = cache_session and bk_token == cache_session.get("bk_token")
            if is_match and request.user.is_authenticated:
                return request.user

        user = auth.authenticate(request=request, bk_token=bk_token)
        if user is not None and user.username != request.user.username:
            auth.login(request, user)

        if user is not None and request.user.is_authenticated:
            if not request.session.session_key:
                # 切换新用户, 重新生成session_key.
                request.session.cycle_key()
            # 登录成功，重新调用自身函数，即可退出
            cache.set(request.session.session_key, {"bk_token": bk_token}, settings.LOGIN_CACHE_EXPIRED)

        return user
