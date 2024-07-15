import time

from utils.munchkin_driver import MunchkinDriver
import json
from loguru import logger


class JenkinsIntegration:
    def __init__(self):
        self.munchkin = MunchkinDriver()

    def list_jenkins_job(self, sender_id):
        result = self.munchkin.automation_skills_execute(
            "list_jenkins_jobs",
            "",
            sender_id)
        keys = result['return'][0].keys()
        first_key = list(keys)[0]
        if result['return'][0][first_key] is False:
            return "自动化任务执行失败"

        jobs = json.loads(result['return'][0][first_key])['jobs']
        table_str = "| 名称 |\n| --- |\n"
        for job in jobs:
            table_str += f"| {job['name']} | \n"
        return table_str

    def analyze_build_log(self, job_name, sender_id):
        build_log = self.get_build_log(job_name, sender_id)
        result = self.munchkin.chat("action_llm_jenkins_build_analysis",
                                    build_log[-10000:], [], sender_id)
        return result

    def get_build_log(self, job_name, sender_id):
        result = self.munchkin.automation_skills_execute(
            "jenkins_last_build_number",
            {"job_name": job_name},
            sender_id)
        keys = result['return'][0].keys()
        first_key = list(keys)[0]
        if result['return'][0][first_key] is False:
            return "自动化任务执行失败"

        build_number = int(result['return'][0][first_key])
        result = self.munchkin.automation_skills_execute(
            "jenkins_build_logs",
            {"job_name": job_name, "build_number": str(build_number)},
            sender_id)
        keys = result['return'][0].keys()
        first_key = list(keys)[0]
        return result['return'][0][first_key]

    def build_jenkins_job(self, job_name, sender_id):
        # 获取最新的构建号
        result = self.munchkin.automation_skills_execute(
            "jenkins_last_build_number",
            {"job_name": job_name},
            sender_id)

        build_number = None
        keys = result['return'][0].keys()
        first_key = list(keys)[0]
        if result['return'][0][first_key] is False:
            return "自动化任务执行失败"
        else:
            build_number = int(result['return'][0][first_key]) + 1
        logger.info(f'构建号：{build_number}')

        # 触发构建任务
        result = self.munchkin.automation_skills_execute(
            "jenkins_build",
            {"job_name": job_name},
            sender_id)
        logger.info(result)
        keys = result['return'][0].keys()
        first_key = list(keys)[0]
        if result['return'][0][first_key] is False:
            return "自动化任务执行失败"

        # 等待构建完成
        while True:
            result = self.munchkin.automation_skills_execute(
                "jenkins_build_status",
                {"job_name": job_name, "build_number": str(build_number)},
                sender_id)
            keys = result['return'][0].keys()
            first_key = list(keys)[0]
            try:
                build_status = json.loads(result['return'][0][first_key])['result']
                if build_status in ['SUCCESS', 'FAILURE']:
                    break
                else:
                    logger.info(f'当前构建状态：{build_status}')
            except Exception as e:
                logger.info('构建任务启动中,请稍等')
            time.sleep(5)

        build_result = self.munchkin.automation_skills_execute(
            "jenkins_build_logs",
            {"job_name": job_name, "build_number": str(build_number)},
            sender_id)
        keys = build_result['return'][0].keys()
        first_key = list(keys)[0]
        logger.info(f'构建结果：{build_result["return"][0][first_key]}')

        return "自动化任务执行成功"
