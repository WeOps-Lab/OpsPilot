# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsMonitor(object):
    """Collections of GSE APIS"""

    def __init__(self, client):
        self.client = client

        self.get_ts_data = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/monitor_v3/get_ts_data/",
            description=u"查询TS",
        )
        self.metadata_get_time_series_group = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/monitor_v3/metadata_get_time_series_group/",
            description=u"获取自定义时序分组具体内容",
        )
