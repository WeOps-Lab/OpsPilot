import time

from utils.munchkin_driver import MunchkinDriver
import json
from loguru import logger


class JenkinsIntegration:
    def __init__(self):
        self.munchkin = MunchkinDriver()

    def list_jenkins_job(self, sender_id):
        try:
            job_list = self.munchkin.execute_single_target_skill(
                "list_jenkins_jobs",
                "",
                sender_id)

            jobs = json.loads(job_list)['jobs']
            table_str = "| 名称 |\n| --- |\n"
            for job in jobs:
                table_str += f"| {job['name']} | \n"
            return table_str
        except Exception as e:
            logger.info(f'获取Jenkins任务列表失败,原因：{e}')
            return f"获取Jenkins任务列表失败,原因：{e}"

    def analyze_build_log(self, job_name, sender_id):
        build_log = self.get_build_log(job_name, sender_id)
        result = self.munchkin.chat("action_llm_jenkins_build_analysis",
                                    build_log[-10000:], [], sender_id)
        return result

    def get_build_log(self, job_name, sender_id):
        last_build_number = self.munchkin.execute_single_target_skill(
            "jenkins_last_build_number",
            {"job_name": job_name},
            sender_id)

        last_build_log = self.munchkin.execute_single_target_skill(
            "jenkins_build_logs",
            {"job_name": job_name, "build_number": str(last_build_number)},
            sender_id)

        return last_build_log

    def build_jenkins_job(self, job_name, sender_id):
        try:
            # 获取最后一次的构建号
            build_number = self.munchkin.execute_single_target_skill(
                "jenkins_last_build_number",
                {"job_name": job_name},
                sender_id)

            # 查看最后一次构建是否还没有完成，假如还没有完成，则告诉用户等待
            build_result = self.munchkin.execute_single_target_skill(
                "jenkins_build_status",
                {"job_name": job_name, "build_number": str(build_number)},
                sender_id)
            build_status = json.loads(build_result)['result']
            if build_status in ['SUCCESS', 'FAILURE']:
                logger.info(f'任务[{job_name}]最后一次构建状态：{build_status}，可以开始新的构建任务')
            else:
                logger.info(f'任务[{job_name}]最后一次构建状态：{build_status}，请等待构建任务完成')
                return f"任务[{job_name}]最后一次构建状态：{build_status}，请等待构建任务完成"

            # 触发构建任务
            self.munchkin.execute_single_target_skill(
                "jenkins_build",
                {"job_name": job_name},
                sender_id)

            target_build_number = str(build_number + 1)
            # 等待构建完成
            while True:
                logger.info(f'查询构建任务[{job_name}]  构建号[{target_build_number}]状态')
                build_status_response = self.munchkin.execute_single_target_skill(
                    "jenkins_build_status",
                    {"job_name": job_name, "build_number": target_build_number},
                    sender_id)
                try:
                    build_status = json.loads(build_status_response)['result']
                    if build_status in ['SUCCESS', 'FAILURE']:
                        logger.info(f'任务[{job_name}] 当前构建状态：{build_status},构建任务完成')
                        break
                    else:
                        logger.info(f'任务[{job_name}] 当前构建状态：{build_status}')
                except Exception as e:
                    logger.info(f'任务[{job_name}]启动中,请稍等')
                time.sleep(5)

            if build_status == 'SUCCESS':
                return f"任务[{job_name}] 当前构建状态：{build_status},构建任务完成"
            else:
                logger.info(f'任务[{job_name}] 当前构建状态：{build_status},构建任务失败,启动构建自动化分析任务')
                analyze_result = self.analyze_build_log(job_name, sender_id)
                return analyze_result
        except Exception as e:
            logger.info(f'任务[{job_name}]构建失败,原因：{e}')
            return f"任务[{job_name}]构建失败,原因：{e}"
