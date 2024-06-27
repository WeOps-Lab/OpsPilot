import yaml
from apps.bot_mgmt.models import Bot
from apps.core.utils.template_loader import core_template
from kubernetes import client, config
from loguru import logger
from nanoid import generate
from rest_framework.authtoken.models import Token

from munchkin.components.conversation_mq import CONVERSATION_MQ_PASSWORD, CONVERSATION_MQ_USER, CONVERSATION_MQ_HOST, \
    CONVERSATION_MQ_PORT
from munchkin.components.kubernetes import KUBE_CONFIG_FILE
from munchkin.components.pilot import MUNCHKIN_BASE_URL


class KubernetesClient:
    def __init__(self, namespace: str = "default"):
        """
        :param namespace: 操作的目标NameSpace
        :param kube_config_file: 目标KubeConfig，不填写则获取默认配置文件路径
        """
        self.namespace = namespace
        if KUBE_CONFIG_FILE == "":
            config.load_kube_config()
        else:
            config.load_kube_config(config_file=KUBE_CONFIG_FILE)

        self.core_api = client.CoreV1Api()
        self.app_api = client.AppsV1Api()
        self.storage_api = client.StorageV1Api()
        self.custom_object_api = client.CustomObjectsApi()
        self.batch_api = client.BatchV1Api()
        self.traefik_resource_group = "traefik.containo.us"

        self.argo_resource_group = "argoproj.io"
        self.argo_resource_version = "v1alpha1"

    def start_pilot(self, bot: Bot):
        logger.info(f"启动Pilot: {bot.id}")

        token = Token.objects.first()
        dynamic_dict = {
            "bot_id": bot.id,
            "api_key": token.key,
            "base_url": MUNCHKIN_BASE_URL,
            "rabbitmq_host": CONVERSATION_MQ_HOST,
            "rabbitmq_port": CONVERSATION_MQ_PORT,
            "rabbitmq_user": CONVERSATION_MQ_USER,
            "rabbitmq_password": CONVERSATION_MQ_PASSWORD,
            "enable_ssl": bot.enable_ssl,
            "bot_domain": bot.bot_domain,
            "enable_nodeport": bot.enable_node_port,
            "web_nodeport": bot.node_port,
        }

        try:
            deployment_template = core_template.get_template("pilot/pilot-deployment.yml")
            deployment = deployment_template.render(dynamic_dict)
            self.app_api.create_namespaced_deployment(namespace="ops-pilot", body=yaml.safe_load(deployment))
            logger.info(f"启动Pilot[{bot.id}]Pod成功")
        except Exception as e:
            logger.error(f"启动Pilot[{bot.id}]Pod失败: {e}")

        try:
            svc_template = core_template.get_template("pilot/pilot-svc.yml")
            svc = svc_template.render(dynamic_dict)
            self.core_api.create_namespaced_service(namespace="ops-pilot", body=yaml.safe_load(svc))
            logger.info(f"启动Pilot[{bot.id}]Service成功")
        except Exception as e:
            logger.error(f"启动Pilot[{bot.id}]Service失败: {e}")

        if bot.enable_bot_domain:
            try:
                ingress_template = core_template.get_template("pilot/pilot-ingress.yml")
                ingress = ingress_template.render(dynamic_dict)
                self.custom_object_api.create_namespaced_custom_object(
                    group=self.traefik_resource_group,
                    version="v1alpha1",
                    plural="ingressroutes",
                    body=yaml.safe_load(ingress),
                    namespace=self.namespace,
                )
                logger.info(f"启动Pilot[{bot.id}]Ingress成功")
            except Exception as e:
                logger.error(f"启动Pilot[{bot.id}]Ingress失败: {e}")

    def stop_pilot(self, bot_id):
        try:
            self.app_api.delete_namespaced_deployment(name=f"pilot-{bot_id}", namespace="ops-pilot")
            logger.info(f"停止Pilot[{bot_id}]Pod成功")
        except Exception as e:
            logger.error(f"停止Pilot[{bot_id}]Pod失败: {e}")

        try:
            self.core_api.delete_namespaced_service(name=f"pilot-{bot_id}-service", namespace="ops-pilot")
            logger.info(f"停止Pilot[{bot_id}]Service成功")
        except Exception as e:
            logger.error(f"停止Pilot[{bot_id}]Service失败: {e}")

        try:
            self.custom_object_api.delete_namespaced_custom_object(
                group=self.traefik_resource_group,
                version="v1alpha1",
                plural="ingressroutes",
                namespace="ops-pilot",
                name=f"pilot-{bot_id}",
            )
        except Exception as e:
            logger.error(f"停止Pilot[{bot_id}]Ingress失败: {e}")

    def train_pilot(self, model_id):
        """
        启动Pilot训练任务
        """
        logger.info(f"启动Pilot模型训练任务: {model_id}")

        uid = generate("1234567890abcdef", 10)
        template = core_template.get_template("pilot/train-pilot.yml")
        token = Token.objects.first()
        workflow_id = f"train-pilot-{uid}"
        dynamic_args = {
            "model_id": model_id,
            "munchkin_token": token.key,
            "workflow_id": workflow_id,
            "munchkin_url": MUNCHKIN_BASE_URL,
        }
        result = template.render(dynamic_args)

        self.custom_object_api.create_namespaced_custom_object(
            group=self.argo_resource_group,
            version=self.argo_resource_version,
            plural="workflows",
            body=yaml.safe_load(result),
            namespace=self.namespace,
        )
        return workflow_id
