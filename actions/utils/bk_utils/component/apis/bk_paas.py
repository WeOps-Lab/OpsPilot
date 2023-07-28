# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsBkPaas(object):
    """Collections of BK_PAAS APIS"""

    def __init__(self, client):
        self.client = client

        self.get_app_info = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/bk_paas/get_app_info/',
            description=u'获取应用信息'
        )
