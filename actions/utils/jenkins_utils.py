from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester
from rasa_sdk import logger

from actions.constants.server_settings import server_settings


class JenkinsUtils:
    def __init__(self):
        self.crumb = CrumbRequester(
            server_settings.jenkins_username,
            server_settings.jenkins_password,
            baseurl=server_settings.jenkins_url,
            ssl_verify=False,
            crumb_requester=True,
        )
        self.jenkins = Jenkins(
            server_settings.jenkins_url,
            username=server_settings.jenkins_username,
            password=server_settings.jenkins_password,
            requester=self.crumb,
        )

    def list_jenkins_job(self):
        jobs = self.jenkins.get_jobs_list()
        return jobs

    def find_jenkins_job(self, job_name):
        return self.jenkins.has_job(job_name)

    def search_jenkins_job(self, job_name):
        jobs = self.jenkins.get_jobs_list()
        if jobs is None:
            return []
        else:
            matching_jobs = []
            for job in jobs:
                if job_name.lower() in job.lower():
                    matching_jobs.append(job)
            return matching_jobs

    def trigger_jenkins_pipeline(self, job_name):
        job = self.jenkins[job_name]
        queue_item = job.invoke()
        queue_item.block_until_building()
        build_number = queue_item.get_build_number()
        logger.info(
            f"启动Jenkins构建任务，任务名称:[{job_name}],构建ID:[{build_number}]"
        )
        return build_number

    def get_jenkins_build_info(self, job_name, build_number):
        job = self.jenkins[job_name]
        build = job.get_build(int(build_number))
        return (
            build.is_running(),
            build.get_status(),
            build.get_timestamp(),
            build.get_estimated_duration(),
        )

    # def analyze_jenkins_build_console(self, job_name, build_number):
    #     job = self.jenkins[job_name]
    #     build = job.get_build(int(build_number))
    #     result = query_chatgpt(
    #         '扮演专业的运维开发工程师，你拥有丰富的运维领域经验，现在你正在使用Jenkins构建项目，出现了以下异常信息，给出你的分析意见以及处置建议.',
    #         build.get_console())
    #     return result
