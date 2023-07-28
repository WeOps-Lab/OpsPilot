# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsGSE(object):
    """Collections of GSE APIS"""

    def __init__(self, client):
        self.client = client

        self.get_agent_info = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi{bk_api_ver}/gse/get_agent_info/',
            description=u'Agent心跳信息查询'
        )
        self.get_agent_status = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi{bk_api_ver}/gse/get_agent_status/',
            description=u'Agent在线状态查询'
        )
        self.proc_create_session = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi{bk_api_ver}/gse/proc_create_session/',
            description=u'进程管理：新建 session'
        )
        self.proc_get_task_result_by_id = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/gse/proc_get_task_result_by_id/',
            description=u'进程管理：获取任务结果'
        )
        self.proc_run_command = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi{bk_api_ver}/gse/proc_run_command/',
            description=u'进程管理：执行命令'
        )
        self.get_proc_operate_result = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi{bk_api_ver}/gse/get_proc_operate_result/',
            description=u'查询进程操作结果'
        )
        self.get_proc_status = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi{bk_api_ver}/gse/get_proc_status/',
            description=u'查询进程状态信息'
        )
        self.operate_proc = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi{bk_api_ver}/gse/operate_proc/',
            description=u'进程操作'
        )
        self.register_proc_info = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi{bk_api_ver}/gse/register_proc_info/',
            description=u'注册进程信息'
        )
        self.unregister_proc_info = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi{bk_api_ver}/gse/unregister_proc_info/',
            description=u'注销进程信息'
        )
        self.update_proc_info = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi{bk_api_ver}/gse/update_proc_info/',
            description=u'更新进程信息'
        )