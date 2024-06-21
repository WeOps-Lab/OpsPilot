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

import traceback

from apps.core.utils.http import send
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db import IntegrityError
from loguru import logger

ROLE_TYPE_ADMIN = "1"


class TokenBackend(ModelBackend):
    def authenticate(self, request=None, bk_token=None):
        logger.debug("Enter in TokenBackend")
        # 判断是否传入验证所需的bk_token,没传入则返回None
        if not bk_token:
            return None

        verify_result, username = self.verify_bk_token(bk_token)
        # 判断bk_token是否验证通过,不通过则返回None
        if not verify_result:
            return None

        try:
            user, _ = User.objects.get_or_create(username=username, is_superuser=True)
            return user

        except IntegrityError:
            logger.exception(traceback.format_exc())
            logger.exception("get_or_create UserModel fail or update_or_create UserProperty")
            return None
        except Exception:  # pylint: disable=broad-except
            logger.exception(traceback.format_exc())
            logger.exception("Auto create & update UserModel fail")
            return None

    @staticmethod
    def verify_bk_token(bk_token):
        """
        请求VERIFY_URL,认证bk_token是否正确
        @param bk_token: "_FrcQiMNevOD05f8AY0tCynWmubZbWz86HslzmOqnhk"
        @type bk_token: str
        @return: False,None True,username
        @rtype: bool,None/str
        """
        api_params = {"bk_token": bk_token}
        verify_url = settings.BK_PAAS_HOST + "/login/accounts/is_login/"
        try:
            response = send(verify_url, api_params, "GET", verify=False)
        except Exception:  # pylint: disable=broad-except
            logger.exception("Abnormal error in verify_bk_token...")
            return False, None

        if response.get("result"):
            data = response.get("data")
            username = data.get("username")
            return True, username
        else:
            error_msg = response.get("message", "")
            error_data = response.get("data", "")
            logger.error("Fail to verify bk_token, error={}, ret={}".format(error_msg, error_data))
            return False, None
