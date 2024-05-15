import inspect
import json
import threading
import uuid
from typing import Text, Optional, Dict, Any, Callable, Awaitable
from urllib.parse import quote
import tiktoken
import requests
from loguru import logger
from rasa.core.channels import InputChannel, UserMessage
from sanic import Blueprint, Request, HTTPResponse, response

from actions.services.chat_service import ChatService


class GitlabReviewChannel(InputChannel):
    def name(self) -> Text:
        return "gitlab_review_channel"

    def __init__(self, token, gitlab_token, fastgpt_url, fastgpt_key, gitlab_url, secret_token) -> None:
        super().__init__()
        self.token = token
        self.gitlab_token = gitlab_token
        self.fastgpt_key = fastgpt_key
        self.gitlab_url = gitlab_url
        self.chat_service = ChatService(fastgpt_url, fastgpt_key)
        self.secret_token = secret_token
        logger.info("GitlabReviewChannel initialized")

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls(
            credentials.get("token"),
            credentials.get("gitlab_token"),
            credentials.get("fastgpt_url"),
            credentials.get("fastgpt_key"),
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

        def num_tokens_from_string(string: str) -> int:
            encoding = tiktoken.get_encoding('cl100k_base')
            num_tokens = len(encoding.encode(string))
            return num_tokens

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
                    changed_files.append({"file_path": file_path, "content": file_content, "diff": change["diff"]})

            changes_string = '\n'.join(
                [f"File: {file['file_path']}\n---\n{file['content']}\n--\nCommit Diff:\n{file['diff']}" for file in
                 changed_files])

            if num_tokens_from_string(changes_string) > 30000:
                logger.warning(f'[{mr_id}] The content of the file is too long to review.')
                return f'[{mr_id}] The content of the file is too long to review.'

            review_msg = self.chat_service.chat(str(uuid.uuid4()), changes_string)
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
            rs = requests.get(commit_url, headers=headers)
            changes = rs.json()

            changed_files = []
            for change in changes:
                if "new_path" in change:  # Use old_path if you want the version before the changes.
                    file_path = change["new_path"]
                    file_content = get_file_content(project_id, file_path, commit_id)
                    changed_files.append({"file_path": file_path, "content": file_content, "diff": change["diff"]})
            changes_string = '\n'.join(
                [f"File: {file['file_path']}\n---\n{file['content']}\n--\nCommit Diff:\n{file['diff']}" for file in
                 changed_files])
            if num_tokens_from_string(changes_string) >= 30000:
                logger.warning(f'[{commit_id}]文件内容过长，不进行审核')
                return f'[{commit_id}]文件内容过长，不进行审核'

            answer = self.chat_service.chat(str(uuid.uuid4()), changes_string)
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

            # TODO:临时用着..
            headers = {"Content-Type": "application/json"}
            requests.post(f'http://localhost:5005/webhooks/notification_bot_channel?secret_token={self.secret_token}',
                          headers=headers,
                          data=json.dumps({"content": content}))

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
