# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsJOB(object):
    """Collections of JOB APIS"""

    def __init__(self, client):
        self.client = client

        self.execute_job = ComponentAPI(
            client=self.client, method="POST", path="/api/c/compapi{bk_api_ver}/job/execute_job/", description=u"启动作业"
        )
        self.fast_execute_sql = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/job/fast_execute_sql/",
            description=u"快速执行SQL脚本",
        )
        self.get_cron_list = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/job/get_cron_list/",
            description=u"查询业务下定时作业信息",
        )
        self.get_job_detail = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/job/get_job_detail/",
            description=u"查询作业模板详情",
        )
        self.get_job_instance_log = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/job/get_job_instance_log/",
            description=u"根据作业实例ID查询作业执行日志",
        )
        self.get_job_instance_status = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/job/get_job_instance_status/",
            description=u"查询作业执行状态",
        )
        self.get_job_list = ComponentAPI(
            client=self.client, method="GET", path="/api/c/compapi{bk_api_ver}/job/get_job_list/", description=u"查询作业模板"
        )
        self.get_os_account = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/job/get_os_account/",
            description=u"查询业务下的执行账号",
        )
        self.get_own_db_account_list = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/job/get_own_db_account_list/",
            description=u"查询用户有权限的DB帐号列表",
        )
        self.get_public_script_list = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/job/get_public_script_list/",
            description=u"查询公共脚本列表",
        )
        self.get_script_detail = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/job/get_script_detail/",
            description=u"查询脚本详情",
        )
        self.get_script_list = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/job/get_script_list/",
            description=u"查询脚本列表",
        )
        self.get_step_instance_status = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/job/get_step_instance_status/",
            description=u"查询作业步骤的执行状态",
        )
        self.update_cron_status = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/job/update_cron_status/",
            description=u"更新定时作业状态",
        )
        self.fast_execute_script = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/job/fast_execute_script/",
            description=u"快速执行脚本",
        )
        self.fast_push_file = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/job/fast_push_file/",
            description=u"快速分发文件",
        )
        self.save_cron = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/job/save_cron/",
            description=u"新建或保存定时作业",
        )
        self.change_cron_status = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/job/change_cron_status/",
            description=u"更新定时作业状态",
        )
        self.execute_task = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/job/execute_task/",
            description=u"根据作业模板ID启动作业",
        )
        self.execute_task_ext = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/job/execute_task_ext/",
            description=u"启动作业Ext(带全局变量启动)",
        )
        self.get_agent_status = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/job/get_agent_status/",
            description=u"查询Agent状态",
        )
        self.get_cron = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/job/get_cron/",
            description=u"查询业务下定时作业信息",
        )
        self.get_task = ComponentAPI(
            client=self.client, method="GET", path="/api/c/compapi{bk_api_ver}/job/get_task/", description=u"查询作业模板"
        )
        self.get_task_detail = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/job/get_task_detail/",
            description=u"查询作业模板详情",
        )
        self.get_task_ip_log = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/job/get_task_ip_log/",
            description=u"根据作业实例ID查询作业执行日志",
        )
        self.get_task_result = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/job/get_task_result/",
            description=u"根据作业实例 ID 查询作业执行状态",
        )
        self.fast_transfer_file = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi/v2/jobv3/fast_transfer_file/",
            description=u"V3快速分发文件",
        )
        self.fast_execute_script_v3 = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/jobv3/fast_execute_script/",
            description=u"快速执行脚本",
        )
        self.get_job_instance_status_v3 = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/jobv3/get_job_instance_status/",
            description=u"根据作业实例 ID 查询作业执行状态",
        )
        self.get_job_instance_ip_log_v3 = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/jobv3/get_job_instance_ip_log/",
            description=u"根据ip查询作业执行日志",
        )
        self.batch_get_job_instance_ip_log_v3 = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/jobv3/batch_get_job_instance_ip_log/",
            description=u"根据ip列表批量查询作业执行日志",
        )
        self.operate_job_instance = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/jobv3/operate_job_instance/",
            description=u"用于对执行的作业实例进行操作，例如终止作业。",
        )
