import inspect
import json
import re
import threading
import uuid
from typing import Text, Optional, Dict, Any, Callable, Awaitable
from urllib.parse import quote

import requests
from loguru import logger
from rasa.core.channels import InputChannel, UserMessage
from sanic import Blueprint, Request, HTTPResponse, response

from core.server_settings import server_settings
from utils.eventbus import EventBus, CODE_REVIEW_EVENT
from utils.munchkin_driver import MunchkinDriver


class GitlabReviewChannel(InputChannel):
    def name(self) -> Text:
        return "gitlab_review_channel"

    def __init__(self, token, gitlab_token, gitlab_url) -> None:
        super().__init__()
        self.token = token
        self.gitlab_token = gitlab_token
        self.gitlab_url = gitlab_url

        self.llm = MunchkinDriver()
        self.event_bus = EventBus()

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls(
            credentials.get("token"),
            credentials.get("gitlab_token"),
            credentials.get('gitlab_url'),
            credentials.get('secret_token')
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

        def filter_diff_content(diff_content):
            filtered_content = re.sub(r'(^-.*\n)', '', diff_content, flags=re.MULTILINE)
            processed_code = '\n'.join(
                [line[1:] if line.startswith('+') else line for line in filtered_content.split('\n')])
            return processed_code

        def handle_merge_request(payload):
            if payload["object_attributes"]["action"] != "open":
                logger.info("Merge request is not open, skipping")
                return response.json({"status": "ok"}, status=200)

            project_id = payload["project"]["id"]
            mr_id = payload["object_attributes"]["iid"]
            changes_url = f"{self.gitlab_url}/projects/{project_id}/merge_requests/{mr_id}/changes"

            logger.info(f'Starting to review merge request: {mr_id}')
            headers = {"Private-Token": self.gitlab_token}
            rs = requests.get(changes_url, headers=headers)
            mr_changes = rs.json()

            changed_files = []
            for change in mr_changes["changes"]:
                if "new_path" in change:  # Use old_path if you want the version before the changes.
                    file_path = change["new_path"]
                    file_content = get_file_content(project_id, file_path,
                                                    payload["object_attributes"]["last_commit"]["id"])
                    changed_files.append(
                        {"file_path": file_path, "content": file_content, "diff": filter_diff_content(change["diff"])})

            changes_string = '\n'.join(
                [f"完整代码: {file['file_path']}\n---\n{file['content']}\n--\n变更部分:\n{file['diff']}" for file in
                 changed_files])

            review_msg = self.llm.chat(
                'gitlab_code_review_action',
                changes_string, '')
            review_msg = f'@{payload["user_username"]}:' + review_msg
            logger.info(f'[{mr_id}]Review result：{review_msg}')

            comment_url = f"{self.gitlab_url}/projects/{project_id}/merge_requests/{mr_id}/notes"
            comment_payload = {"body": review_msg}
            comment_response = requests.post(comment_url, headers=headers, json=comment_payload)
            comment_response.raise_for_status()
            logger.info(f"Posted review message for merge request {mr_id}")
            return review_msg

        def get_file_content(project_id, file_path, commit_id):
            quoted_file_path = quote(file_path, safe='')
            file_url = f"{self.gitlab_url}/projects/{project_id}/repository/files/{quoted_file_path}/raw?ref={commit_id}"
            headers = {"Private-Token": self.gitlab_token}
            rs = requests.get(file_url, headers=headers)
            return rs.text

        def handle_push(payload):
            project_id = payload["project_id"]
            commit_id = payload["after"]
            commit_url = f"{self.gitlab_url}/projects/{project_id}/repository/commits/{commit_id}/diff"

            logger.info(f'开始审核commit: {commit_id}')
            headers = {"Private-Token": self.gitlab_token}
            rs = requests.get(commit_url, headers=headers, )
            changes = rs.json()

            changed_files = []
            for change in changes:
                if "new_path" in change:  # Use old_path if you want the version before the changes.
                    file_path = change["new_path"]
                    file_content = get_file_content(project_id, file_path, commit_id)
                    changed_files.append(
                        {"file_path": file_path, "content": file_content, "diff": filter_diff_content(change["diff"])})
            changes_string = '\n'.join(
                [f"完整代码: {file['file_path']}\n---\n{file['content']}\n--\n 变更部分 :\n{file['diff']}" for file in
                 changed_files])

            answer = self.llm.chat('gitlab_code_review_action', changes_string, '')
            answer = f'@{payload["user_username"]}:' + answer
            logger.info(f'[{commit_id}]审核结果：{answer}')

            comment_url = f"{self.gitlab_url}/projects/{project_id}/repository/commits/{commit_id}/comments"
            comment_payload = {"note": answer}
            comment_response = requests.post(comment_url, headers=headers, json=comment_payload)
            comment_response.raise_for_status()
            logger.info(f"Posted comment for commit {commit_id}")
            return answer

        def handle_request(payload):
            try:
                if payload.get("object_kind") == "merge_request":
                    content = handle_merge_request(payload)
                elif payload.get("object_kind") == "push":
                    content = handle_push(payload)
            except Exception as e:
                content = f'Reivew失败: {str(e)}'
            self.event_bus.publist_notification_event()
            self.event_bus.publish(
                json.dumps({
                    "notification_content": f'@{payload["user_username"].split("[")[0]} {content}',
                    "event_type": CODE_REVIEW_EVENT
                }))

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
