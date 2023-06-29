from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester
from rasa_sdk import logger

from actions.constant.server_settings import server_settings
from actions.utils.langchain_utils import query_chatgpt


def get_jenkins_instance():
    crumb = CrumbRequester(server_settings.jenkins_username, server_settings.jenkins_password,
                           baseurl=server_settings.jenkins_url, ssl_verify=False, crumb_requester=True)
    jenkins = Jenkins(server_settings.jenkins_url, username=server_settings.jenkins_username,
                      password=server_settings.jenkins_password, requester=crumb)
    return jenkins


def get_jenkins_build_info(job_name, build_number):
    jenkins = get_jenkins_instance()
    job = jenkins[job_name]
    build = job.get_build(int(build_number))
    return build.is_running(), build.get_status(), \
        build.get_timestamp(), build.get_estimated_duration()


def analyze_jenkins_build_console(job_name, build_number):
    jenkins = get_jenkins_instance()
    job = jenkins[job_name]
    build = job.get_build(int(build_number))
    result = query_chatgpt([
        {"role": "system",
         "content": "扮演专业的运维开发工程师，你拥有丰富的运维领域经验，现在你正在使用Jenkins构建项目，出现了以下异常信息，给出你的分析意见以及处置建议."},
        {"role": "user", "content": build.get_console()},
    ])
    return result


def find_jenkins_job(job_name):
    jenkins = get_jenkins_instance()
    return jenkins.has_job(job_name)


def list_jenkins_job():
    jenkins = get_jenkins_instance()
    jobs = jenkins.get_jobs_list()
    return jobs


def search_jenkins_job(job_name):
    jenkins = get_jenkins_instance()
    jobs = jenkins.get_jobs_list()
    if jobs is None:
        return []
    else:
        matching_jobs = []
        for job in jobs:
            if job_name.lower() in job.lower():
                matching_jobs.append(job)
        return matching_jobs


def trigger_jenkins_pipeline(job_name):
    jenkins = get_jenkins_instance()
    job = jenkins[job_name]
    queue_item = job.invoke()
    queue_item.block_until_building()
    build_number = queue_item.get_build_number()
    logger.info(f"启动Jenkins构建任务，任务名称:[{job_name}],构建ID:[{build_number}]")
    return build_number
