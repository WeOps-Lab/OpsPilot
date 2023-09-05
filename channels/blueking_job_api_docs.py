job_api_desc = """
作业平台（Job）是一套基于蓝鲸智云管控平台Agent管道之上的基础操作平台，具备大并发处理能力；除了支持脚本执行、文件拉取/分发、定时任务等一系列可实现的基础运维场景以外，还运用流程化的理念很好的将零碎的单个任务组装成一个作业流程；而每个任务都可做为一个原子节点，提供给其它系统和平台调度，实现调度自动化。
资源名称	资源描述
batch_get_job_instance_ip_log	根据ip列表批量查询作业执行日志
callback_protocol	作业类回调报文描述
execute_job_plan	执行作业执行方案
fast_execute_script	快速执行脚本
fast_execute_sql	快速执行SQL
fast_transfer_file	快速分发文件
get_account_list	查询业务下的执行账号
get_cron_detail	查询定时作业详情
get_cron_list	查询业务下定时作业信息
get_job_instance_global_var_value	获取作业实例全局变量值
get_job_instance_ip_log	根据作业实例ID查询作业执行日志
get_job_instance_list	查询作业实例列表(执行历史)
get_job_instance_status	根据作业实例 ID 查询作业执行状态
get_job_plan_detail	查询执行方案详情
get_job_plan_list	查询执行方案列表
get_job_template_list	查询作业模版列表
get_public_script_list	查询公共脚本列表
get_public_script_version_detail	查询公共脚本详情
get_public_script_version_list	查询公共脚本版本列表
get_script_list	查询脚本列表
get_script_version_detail	查询脚本详情
get_script_version_list	查询脚本版本列表
operate_job_instance	作业实例操作
operate_step_instance	步骤实例操作
save_cron	新建或保存定时作业
update_cron_status	更新定时作业状态，如启动或暂停
"""

get_job_plan_list = """
请求地址
https://paas.cwbk.com/api/c/compapi/v2/jobv3/get_job_plan_list/


请求方法
GET

功能描述
查询执行方案列表

接口参数
字段	类型	必选	描述
bk_biz_id	long	是	业务ID
job_template_id	long	否	作业模版 ID
creator	string	否	作业执行方案创建人帐号
name	string	否	作业执行方案名称，模糊匹配
create_time_start	long	否	创建起始时间，Unix 时间戳
create_time_end	long	否	创建结束时间，Unix 时间戳
last_modify_user	string	否	作业执行方案修改人帐号
last_modify_time_start	long	否	最后修改起始时间，Unix 时间戳
last_modify_time_end	long	否	最后修改结束时间，Unix 时间戳
start	int	否	默认0表示从第1条记录开始返回
length	int	否	单次返回最大记录数，最大1000，不传默认为5
请求参数示例
{
  "bk_biz_id": 1,
  "job_template_id": 1,
  "creator": "admin",
  "name": "test",
  "create_time_start": 1546272000000,
  "create_time_end": 1577807999999,
  "last_modify_user": "admin",
  "last_modify_time_start": 1546272000000,
  "last_modify_time_end": 1577807999999,
  "start": 0,
  "length": 20
}
返回结果示例
{
    "result": true, 
    "code": 0, 
    "message": "success", 
    "data": {
        "data": [
            {
                "bk_biz_id": 1, 
                "id": 100, 
                "job_template_id": 1, 
                "name": "test", 
                "creator": "admin", 
                "create_time": 1546272000000, 
                "last_modify_user": "admin", 
                "last_modify_time": 1546272000000
            }
        ], 
        "start": 0, 
        "length": 20, 
        "total": 1
    }
}
返回结果参数说明
data
字段	类型	描述
bk_biz_id	long	业务 ID
id	long	执行方案 ID
job_template_id	long	作业模版 ID
name	string	执行方案名称
creator	string	创建人帐号
create_time	long	创建时间，Unix 时间戳
last_modify_user	string	修改人帐号
last_modify_time	long	最后修改时间，Unix 时间戳
"""
execute_job_plan = """
请求地址
https://paas.cwbk.com/api/c/compapi/v2/jobv3/execute_job_plan/

请求方法
POST

功能描述
启动作业执行方案

接口参数
字段	类型	必选	描述
bk_biz_id	long	是	业务ID
job_plan_id	long	是	作业执行方案ID
global_var_list	array	否	全局变量。对于作业执行方案中的全局变量值，如果请求参数中包含该变量，则使用传入的变量值；否则使用执行方案当前已配置的默认值。定义见global_var
callback_url	string	否	回调URL，当任务执行完成后，JOB会调用该URL告知任务执行结果。回调协议参考callback_protocol组件文档
global_var
字段	类型	必选	描述
id	long	否	全局变量id，唯一标识。如果id为空，那么使用name作为唯一标识
name	string	否	全局变量name
value	string	否	字符、密码、数组、命名空间类型的全局变量的值
server	object	否	主机类型全局变量的值，见server定义
server
字段	类型	必选	描述
ip_list	array	否	静态 IP 列表，定义见ip
dynamic_group_list	array	否	动态分组列表，定义见dynamic_group
topo_node_list	array	否	动态 topo 节点列表，定义见topo_node
ip
字段	类型	必选	描述
bk_cloud_id	int	是	云区域ID
ip	string	是	IP地址
dynamic_group
字段	类型	必选	描述
id	string	是	CMDB动态分组ID
topo_node
字段	类型	必选	描述
id	long	是	动态topo节点ID，对应CMDB API 中的 bk_inst_id
node_type	string	是	动态topo节点类型，对应CMDB API 中的 bk_obj_id,比如"module","set"
请求参数示例
{
    "bk_biz_id": 1,
    "job_plan_id": 100,
    "global_var_list": [
        {
            "id": 436,
            "server": {
                "dynamic_group_list": [
                    {
                        "id": "blo8gojho0skft7pr5q0"
                    }
                ],
                "ip_list": [
                    {
                        "bk_cloud_id": 0,
                        "ip": "10.0.0.1"
                    },
                    {
                        "bk_cloud_id": 0,
                        "ip": "10.0.0.2"
                    }
                ],
                "topo_node_list": [
                    {
                        "id": 1000,
                        "node_type": "module"
                    }
                ]
            }
        },
        {
            "name": "param_name",
            "value": "param_value"
        }
    ]
}
返回结果示例
{
    "result": true,
    "code": 0,
    "message": "success",
    "data": {
        "job_instance_name": "Test",
        "job_instance_id": 10000
    }
}
"""

get_job_instance_status = """
请求地址
https://paas.cwbk.com/api/c/compapi/v2/jobv3/get_job_instance_status/

请求方法
GET

功能描述
根据作业实例 ID 查询作业执行状态

接口参数
字段	类型	必选	描述
bk_biz_id	long	是	业务ID
job_instance_id	long	是	作业实例ID
return_ip_result	boolean	否	是否返回每个ip上的任务详情，对应返回结果中的step_ip_result_list。默认值为false。
请求参数示例
{
    "bk_biz_id": 1,
    "job_instance_id": 100
}
返回结果示例
{
    "result": true,
    "code": 0,
    "message": "",
    "data": {
        "finished": true,
        "job_instance": {
            "job_instance_id": 100,
            "bk_biz_id": 1,
            "name": "API Quick execution script1521089795887",
            "create_time": 1605064271000,
            "status": 4,
            "start_time": 1605064271000,
            "end_time": 1605064272000,
            "total_time": 1000
        },
        "step_instance_list": [
            {
                "status": 4,
                "total_time": 1000,
                "name": "API Quick execution scriptxxx",
                "step_instance_id": 75,
                "execute_count": 0,
                "create_time": 1605064271000,
                "end_time": 1605064272000,
                "type": 1,
                "start_time": 1605064271000,
                "step_ip_result_list": [
                    {
                        "ip": "10.0.0.1",
                        "bk_cloud_id": 0,
                        "status": 9,
                        "tag": "",
                        "exit_code": 0,
                        "error_code": 0,
                        "start_time": 1605064271000,
                        "end_time": 1605064272000,
                        "total_time": 1000
                    }
                ]
            }
        ]
    }
}
返回结果参数说明
data
字段	类型	描述
finished	bool	作业是否结束
job_instance	object	作业实例基本信息。见job_instance定义
step_instance_list	array	作业步骤列表。见step_instance定义
job_instance
字段	类型	描述
name	string	作业实例名称
status	int	作业状态码: 1.未执行; 2.正在执行; 3.执行成功; 4.执行失败; 5.跳过; 6.忽略错误; 7.等待用户; 8.手动结束; 9.状态异常; 10.步骤强制终止中; 11.步骤强制终止成功
create_time	long	作业创建时间，Unix时间戳，单位毫秒
start_time	long	开始执行时间，Unix时间戳，单位毫秒
end_time	long	执行结束时间，Unix时间戳，单位毫秒
total_time	int	总耗时，单位毫秒
bk_biz_id	long	业务ID
job_instance_id	long	作业实例ID
step_instance
字段	类型	描述
step_instance_id	long	作业步骤实例ID
type	int	步骤类型：1.脚本步骤; 2.文件步骤; 4.SQL步骤
name	string	步骤名称
status	int	作业步骤状态码: 1.未执行; 2.正在执行; 3.执行成功; 4.执行失败; 5.跳过; 6.忽略错误; 7.等待用户; 8.手动结束; 9.状态异常; 10.步骤强制终止中; 11.步骤强制终止成功; 12.步骤强制终止失败
create_time	long	作业步骤实例创建时间，Unix时间戳，单位毫秒
start_time	long	开始执行时间，Unix时间戳，单位毫秒
end_time	long	执行结束时间，Unix时间戳，单位毫秒
total_time	int	总耗时，单位毫秒
execute_count	int	步骤重试次数
step_ip_result_list	array	每个主机的任务执行结果，定义见step_ip_result
step_ip_result
字段	类型	描述
ip	string	IP
bk_cloud_id	long	云区域ID
status	int	作业执行状态:1.Agent异常; 5.等待执行; 7.正在执行; 9.执行成功; 11.执行失败; 12.任务下发失败; 403.任务强制终止成功; 404.任务强制终止失败
tag	string	用户通过job_success/job_fail函数模板自定义输出的结果。仅脚本任务存在该参数
exit_code	int	脚本任务exit code
error_code	int	主机任务状态码，1.Agent异常; 3.上次已成功; 5.等待执行; 7.正在执行; 9.执行成功; 11.任务失败; 12.任务下发失败; 13.任务超时; 15.任务日志错误; 101.脚本执行失败; 102.脚本执行超时; 103.脚本执行被终止; 104.脚本返回码非零; 202.文件传输失败; 203.源文件不存在; 310.Agent异常; 311.用户名不存在; 320.文件获取失败; 321.文件超出限制; 329.文件传输错误; 399.任务执行出错
start_time	long	开始执行时间，Unix时间戳，单位毫秒
end_time	long	执行结束时间，Unix时间戳，单位毫秒
total_time	int	总耗时，单位毫秒
"""

get_job_instance_ip_log = """
请求地址
https://paas.cwbk.com/api/c/compapi/v2/jobv3/get_job_instance_ip_log/

请求方法
GET

功能描述
根据ip查询作业执行日志

接口参数
字段	类型	必选	描述
bk_biz_id	long	是	业务ID
job_instance_id	long	是	作业实例ID
step_instance_id	long	是	步骤实例ID
bk_cloud_id	int	是	目标服务器云区域ID
ip	string	是	目标服务器IP
请求参数示例
{
    "bk_biz_id": 1,
    "job_instance_id": 50,
    "step_instance_id": 100,
    "bk_cloud_id": 0,
    "ip": "10.0.0.1"
}
返回结果示例
脚本执行步骤
{
    "result": true,
    "code": 0,
    "message": "",
    "data": {
        "log_type": 1,
        "ip": "10.0.0.1",
        "bk_cloud_id": 0,
        "log_content": "[2018-03-15 14:39:30][PID:56875] job_start\n"
    }
}
文件分发步骤
{
    "result": true,
    "code": 0,
    "message": "",
    "data": {
        "log_type": 2,
        "ip": "10.0.0.1",
        "bk_cloud_id": 0,
        "file_logs": [
            {
                "mode": 1, 
                "src_ip": {
                    "bk_cloud_id": 0, 
                    "ip": "10.0.0.2"
                }, 
                "src_path": "/data/1.log", 
                "dest_ip": {
                    "bk_cloud_id": 0, 
                    "ip": "10.0.0.1"
                }, 
                "dest_path": "/tmp/1.log", 
                "status": 4,
                "log_content": "[2021-06-28 11:32:16] FileName: /tmp/1.log FileSize: 9.0 Bytes State: dest agent success download file Speed: 1 KB/s Progress: 100% StatusDesc: dest agent success download file Detail: success" 
            }, 
            {
                "mode": 0, 
                "src_ip": {
                    "bk_cloud_id": 0, 
                    "ip": "10.0.0.2"
                }, 
                "src_path": "/data/1.log",  
                "status": 4,
                "log_content": "[2021-06-28 11:32:16] FileName: /data/1.log FileSize: 9.0 Bytes State: source agent success upload file Speed: 1 KB/s Progress: 100% StatusDesc: source agent success upload file Detail: success upload"
            }
        ]
    }
}
返回结果说明

文件分发日志，除了目标服务器的文件下载任务日志，也会返回源服务器的文件上传任务日志(mode=0)
dest_ip 与请求参数的bk_cloud_id/ip对应
返回结果参数说明
data
字段	类型	描述
bk_cloud_id	int	目标服务器云区域ID
ip	string	目标服务器IP地址
log_type	int	日志类型。1-脚本执行任务日志;2-文件分发任务日志
log_content	string	作业脚本输出的日志内容
file_logs	array	文件分发任务日志。定义见file_log
file_log
字段	类型	描述
mode	分发模式	0:上传;1:下载
src_ip	object	文件源主机IP。定义见ip
src_path	string	源文件路径
dest_ip	object	分发目标主机IP，mode=1时有值。定义见ip
dest_path	string	目标路径，mode=1时有值
status	int	任务状态。1-等待开始;2-上传中;3-下载中;4-成功;5-失败
log_content	string	文件分发日志内容
ip
字段	类型	描述
bk_cloud_id	long	云区域ID
ip	string	IP地址
"""