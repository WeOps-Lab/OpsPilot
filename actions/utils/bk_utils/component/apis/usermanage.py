# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsUSERMANAGE(object):
    """Collections of USERMANAGE APIS"""

    def __init__(self, client):
        self.client = client

        self.department_ancestor = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/usermanage/department_ancestor/',
            description=u'查询部门全部祖先'
        )
        self.list_department_profiles = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/usermanage/list_department_profiles/',
            description=u'查询部门的用户信息 (v2)'
        )
        self.list_departments = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/usermanage/list_departments/',
            description=u'查询部门 (v2)'
        )
        self.list_profile_departments = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/usermanage/list_profile_departments/',
            description=u'查询用户的部门信息 (v2)'
        )
        self.list_users = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/usermanage/list_users/',
            description=u'查询用户 (v2)'
        )
        self.retrieve_department = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/usermanage/retrieve_department/',
            description=u'查询单个部门信息 (v2)'
        )
        self.retrieve_user = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/compapi{bk_api_ver}/usermanage/retrieve_user/',
            description=u'查询单个用户信息 (v2)'
        )
