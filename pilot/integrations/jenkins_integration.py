from utils.munchkin_driver import MunchkinDriver
import json


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
