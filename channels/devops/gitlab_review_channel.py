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
                return response.json({"status": "ok"}, status=200)
            else:
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
            review_msg = self.chat_service.chat('reviewer', diffs)
            comment_url = f"{self.gitlab_url}/projects/{project_id}/merge_requests/{mr_id}/notes"
            comment_payload = {"body": review_msg}
            comment_response = requests.post(comment_url, headers=headers, json=comment_payload)

        def handle_push(payload):
            project_id = payload["project_id"]
            commit_id = payload["after"]
            commit_url = f"{self.gitlab_url}/projects/{project_id}/repository/commits/{commit_id}/diff"

            headers = {"Private-Token": self.gitlab_token}
            rs = requests.get(commit_url, headers=headers)
            changes = rs.json()
            changes_string = ''.join([str(change) for change in changes])
            answer = self.chat_service.chat('reviewer', changes_string)
            comment_url = f"{self.gitlab_url}/projects/{project_id}/repository/commits/{commit_id}/comments"
            comment_payload = {"note": answer}
            comment_response = requests.post(comment_url, headers=headers, json=comment_payload)

        def handle_request(payload):
            if payload.get("object_kind") == "merge_request":
                handle_merge_request(payload)
            elif payload.get("object_kind") == "push":
                handle_push(payload)

        @hook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            verify_token = request.headers.get('X-Gitlab-Token')
            if verify_token != self.token:
                return response.json({"status": "error"}, status=401)
            payload = request.json
            threading.Thread(target=handle_request, args=(payload,)).start()
            return response.json({"status": "ok"}, status=200)

        return hook
