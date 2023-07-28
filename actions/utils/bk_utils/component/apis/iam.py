# -*- coding: utf-8 -*-
import logging

from ..base import ComponentAPI
from ..exceptions import ComponentAPIException

logger = logging.getLogger("component")


class ComponentAPIV2(ComponentAPI):
    def get_url_with_api_ver(self, data):
        grade_manager_id, group_id = data.get("grade_manager_id", ""), data.get("group_id", "")
        bk_api_ver = self.client.get_bk_api_ver()
        sub_path = "/{}".format(bk_api_ver) if bk_api_ver else ""
        return self.host + self.path.format(bk_api_ver=sub_path, grade_manager_id=grade_manager_id, group_id=group_id)

    def __call__(self, *args, **kwargs):
        self.url = self.get_url_with_api_ver(*args, **kwargs)
        try:
            return self._call(*args, **kwargs)
        except ComponentAPIException as e:
            # Combine log message
            log_message = [e.error_message, "url={url}".format(url=e.api_obj.url)]
            if e.resp:
                log_message.append("content: %s" % e.resp.text)

            logger.exception("\n".join(log_message))

            # Try return error message from remote service
            if e.resp is not None:
                try:
                    return e.resp.json()
                except (TypeError, ValueError):
                    pass
            return {"result": False, "message": e.error_message, "data": None}


class CollectionsIAM(object):
    def __init__(self, client):
        self.client = client

        self.create_grade_manager = ComponentAPIV2(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/iam/management/grade_managers/",
            description=u"创建分级管理员",
        )

        self.get_grade_manager_members = ComponentAPIV2(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/iam/management/grade_managers/{grade_manager_id}/members/",
            description=u"查询分级管理员成员列表",
        )

        self.add_grade_manager_members = ComponentAPIV2(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/iam/management/grade_managers/{grade_manager_id}/members/",
            description=u"添加分级管理员成员",
        )

        self.delete_grade_manager_members = ComponentAPIV2(
            client=self.client,
            method="DELETE",
            path="/api/c/compapi{bk_api_ver}/iam/management/grade_managers/{grade_manager_id}/members/",
            description=u"删除分级管理员成员",
        )

        self.create_user_groups = ComponentAPIV2(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/iam/management/grade_managers/{grade_manager_id}/groups/",
            description=u"创建分级管理员下的用户组",
        )

        self.get_user_groups = ComponentAPIV2(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/iam/management/grade_managers/{grade_manager_id}/groups/",
            description=u"查询分级管理员下的用户组",
        )

        self.update_user_group = ComponentAPIV2(
            client=self.client,
            method="PUT",
            path="/api/c/compapi{bk_api_ver}/iam/management/groups/{group_id}/",
            description=u"更新用户组名称和描述",
        )

        self.delete_user_group = ComponentAPIV2(
            client=self.client,
            method="DELETE",
            path="/api/c/compapi{bk_api_ver}/iam/management/groups/{group_id}/",
            description=u"删除用户组",
        )

        self.get_user_group_members = ComponentAPIV2(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/iam/management/groups/{group_id}/members/",
            description=u"查询用户组成员列表",
        )

        self.add_user_group_members = ComponentAPIV2(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/iam/management/groups/{group_id}/members/",
            description=u"添加用户组成员",
        )

        self.delete_user_group_members = ComponentAPIV2(
            client=self.client,
            method="DELETE",
            path="/api/c/compapi{bk_api_ver}/iam/management/groups/{group_id}/members/",
            description=u"删除用户组成员",
        )

        self.user_group_policies = ComponentAPIV2(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/iam/management/groups/{group_id}/policies/",
            description=u"用户组授权",
        )

        self.get_user_grade_managers = ComponentAPIV2(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/iam/management/users/grade_managers/",
            description=u"查询用户的分级管理员列表",
        )

        self.get_user_grade_manager_user_groups = ComponentAPIV2(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/iam/management/users/grade_managers/{grade_manager_id}/groups/",
            description=u"查询用户在某个分级管理员下的加入的用户组列表",
        )

        self.create_user_group_application = ComponentAPIV2(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/iam/management/groups/applications/",
            description=u"创建用户组申请单据",
        )
