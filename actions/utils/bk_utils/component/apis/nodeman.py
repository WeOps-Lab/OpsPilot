# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsNodeMan(object):
    """Collections of NodeMan APIS"""

    def __init__(self, client):
        self.client = client

        self.search_host = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/nodeman/api/host/search/",
            description=u"查询主机",
        )

        self.get_agent_status_info = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/nodeman/api/host/search/",
            description=u"Agent状态信息查询",
        )

        self.action_agent = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/nodeman/api/job/install/",
            description=u"Agent操作管理",
        )

        self.get_agent_action_detail = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/nodeman/api/job/details/",
            description=u"查询操作作业日志",
        )

        self.get_agent_cation_log = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/nodeman/api/job/log/",
            description=u"查询操作执行日志",
        )

        self.get_ap = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/nodeman/api/ap/",
            description=u"查询接入点列表",
        )

        self.gent_cloud = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/nodeman/api/cloud/",
            description=u"查询云区域",
        )
