from typing import List, Set

import yaml
from pydantic import BaseModel
from nanoid import generate
from apps.core.utils.template_loader import core_template
from munchkin.components.kubernetes import KUBE_CONFIG_FILE
from kubernetes import config, client
from rest_framework.authtoken.models import Token


class KubernetesClient:
    def __init__(self, namespace: str = 'default'):
        """
        :param namespace: 操作的目标NameSpace
        :param kube_config_file: 目标KubeConfig，不填写则获取默认配置文件路径
        """
        self.namespace = namespace
        if KUBE_CONFIG_FILE == '':
            config.load_kube_config()
        else:
            config.load_kube_config(config_file=KUBE_CONFIG_FILE)

        self.core_api = client.CoreV1Api()
        self.app_api = client.AppsV1Api()
        self.storage_api = client.StorageV1Api()
        self.custom_object_api = client.CustomObjectsApi()
        self.batch_api = client.BatchV1Api()
        self.traefik_resource_group = 'traefik.containo.us'

        self.argo_resource_group = 'argoproj.io'
        self.argo_resource_version = "v1alpha1"

    def train_pilot(self, bot_id):
        """
        启动Pilot训练任务
        """
        uid = generate('1234567890abcdef', 10)
        template = core_template.get_template('pilot/train-pilot.yml')
        token = Token.objects.first()
        workflow_id = f'train-pilot-{uid}'
        dynamic_args = {
            "bot_id": bot_id,
            "munchkin_token": token.key,
            "workflow_id": workflow_id
        }
        result = template.render(dynamic_args)

        self.custom_object_api.create_namespaced_custom_object(group=self.argo_resource_group,
                                                               version=self.argo_resource_version,
                                                               plural="workflows",
                                                               body=yaml.safe_load(result),
                                                               namespace=self.namespace)
        return workflow_id
