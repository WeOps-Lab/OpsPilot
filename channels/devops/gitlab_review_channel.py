import inspect
import threading
from typing import Text, Optional, Dict, Any, Callable, Awaitable

import requests
from loguru import logger
from rasa.core.channels import InputChannel, UserMessage
from sanic import Blueprint, Request, HTTPResponse, response

from actions.services.chat_service import ChatService


class GitlabReviewChannel(InputChannel):
    def name(self) -> Text:
        return "gitlab_review_channel"

    def __init__(self, token, gitlab_token, fastgpt_url, fastgpt_key, gitlab_url) -> None:
        super().__init__()
        self.token = token
        self.gitlab_token = gitlab_token
        self.fastgpt_key = fastgpt_key
        self.gitlab_url = gitlab_url
        self.chat_service = ChatService(fastgpt_url, fastgpt_key)
        self.prompt = '''
        以下是供审查的合并请求中的代码片段。 请根据以下标准评估代码：
            语法和风格：检查是否有任何语法错误或与标准编码约定的偏差。 突出显示任何不符合该语言的可读性和可维护性最佳实践的代码行。
            性能优化：确定代码中可以优化以获得更好性能的任何部分。 建议可以提高效率的具体更改，例如优化循环、降低计算复杂性或最小化内存使用量。
            安全实践：扫描代码中常见的安全漏洞，例如 SQL 注入、跨站点脚本 (XSS) 或对用户输入的不当处理。 在适用的情况下推荐安全编码实践。
            错误处理：评估代码是否有正确的错误处理机制。 指出任何可能破坏程序执行流程的潜在未处理异常或错误。
            代码质量：评估代码的整体质量。 寻找代码异味、不必要的复杂性或可以简化或重构的冗余代码。
            错误检测：分析代码是否存在可能导致错误行为的潜在错误或逻辑错误。 解释任何已发现的问题并提出修复建议。
            我希望你能在 100 字之内简洁地总结一下差异。 如果适用，您的摘要应包含有关导出函数签名、全局数据结构和变量的更改以及可能影响代码的外部接口或行为的任何更改的注释。
        确保您的反馈清晰、简洁且可操作，并尽可能提供具体的改进建议，改进建议使用中文回答。
        注意：如果代码问题不是太大，你只需要回答“LGTM”。
        代码：
        '''

        logger.info("GitlabReviewChannel initialized")

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls(
            credentials.get("token"),
            credentials.get("gitlab_token"),
            credentials.get("fastgpt_url"),
            credentials.get("fastgpt_key"),
            credentials.get('gitlab_url')
        )

    def blueprint(
            self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        hook = Blueprint(
            "gitlab_review_channel_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @hook.route("/", methods=["GET"])
        async def index(request: Request) -> HTTPResponse:
            if request.headers.get('X-Gitlab-Token') == self.token:
                logger.info("Token verification successful")
                return response.json({"status": "ok"}, status=200)
            else:
                logger.warning("Token verification failed")
                return response.json({"status": "error"}, status=401)

        def handle_merge_request(payload):
            if payload["object_attributes"]["action"] != "open":
                logger.info("Merge request is not open, skipping")
                return response.json({"status": "ok"}, status=200)

            project_id = payload["project"]["id"]
            mr_id = payload["object_attributes"]["iid"]
            changes_url = f"{self.gitlab_url}/projects/{project_id}/merge_requests/{mr_id}/changes"

            headers = {"Private-Token": self.gitlab_token}
            rs = requests.get(changes_url, headers=headers)
            mr_changes = rs.json()
            diffs = [change["diff"] for change in mr_changes["changes"]]
            diffs = "\n".join(diffs)
            review_msg = self.chat_service.chat('reviewer', self.prompt + diffs)
            logger.info(f'审核结果：{review_msg}')
            comment_url = f"{self.gitlab_url}/projects/{project_id}/merge_requests/{mr_id}/notes"
            comment_payload = {"body": review_msg}
            comment_response = requests.post(comment_url, headers=headers, json=comment_payload)
            logger.info(f"Posted review message for merge request {mr_id}")

        def handle_push(payload):
            project_id = payload["project_id"]
            commit_id = payload["after"]
            commit_url = f"{self.gitlab_url}/projects/{project_id}/repository/commits/{commit_id}/diff"

            headers = {"Private-Token": self.gitlab_token}
            rs = requests.get(commit_url, headers=headers)
            changes = rs.json()
            changes_string = ''.join([str(change) for change in changes])
            answer = self.chat_service.chat('reviewer', self.prompt + changes_string)
            logger.info(f'审核结果：{answer}')

            comment_url = f"{self.gitlab_url}/projects/{project_id}/repository/commits/{commit_id}/comments"
            comment_payload = {"note": answer}
            comment_response = requests.post(comment_url, headers=headers, json=comment_payload)
            logger.info(f"Posted comment for commit {commit_id}")

        def handle_request(payload):
            if payload.get("object_kind") == "merge_request":
                handle_merge_request(payload)
            elif payload.get("object_kind") == "push":
                handle_push(payload)

        @hook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            verify_token = request.headers.get('X-Gitlab-Token')
            if verify_token != self.token:
                logger.warning("Token verification failed")
                return response.json({"status": "error"}, status=401)
            payload = request.json
            threading.Thread(target=handle_request, args=(payload,)).start()
            logger.info("Received webhook, started new thread to handle request")
            return response.json({"status": "ok"}, status=200)

        return hook
