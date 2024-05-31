from typing import List, Set

from pydantic import BaseModel

from munchkin.components.kubernetes import KUBE_CONFIG_FILE
from kubernetes import config, client


class StorageClassDetail(BaseModel):
    name: str
    reclaim_policy: str


class PodInfo(BaseModel):
    name: str
    namespace: str
    ip: str
    startup_time: str
    ide_type: str
    ide_id: str


class NodeInfo(BaseModel):
    labels: dict
    node_name: str
    gpu: int
    docker_version: str
    kernel_version: str
    os_image: str
    ip: str


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

    def list_storage_classes(self) -> List[StorageClassDetail]:
        """
        获取StorageClass的列表
        @return:
        """
        storage_classes = self.storage_api.list_storage_class()
        results = []
        for sc in storage_classes.items:
            results.append(StorageClassDetail(
                name=sc.metadata.name,
                reclaim_policy=sc.reclaim_policy
            ))
        return results

    def list_node_ports(self) -> Set:
        node_ports = set()
        services = self.core_api.list_namespaced_service(self.namespace)
        for service in services.items:
            if service.spec.type == 'NodePort':
                for port in service.spec.ports:
                    node_ports.add(port.node_port)
        return node_ports

    def list_node_info(self) -> List[NodeInfo]:
        """
        获取K8S中节点的信息,以及节点中的IDE列表
        """
        node_infos = []
        nodes = self.core_api.list_node()

        for node in nodes.items:
            labels = node.metadata.labels
            ip_address = next((x.address for x in node.status.addresses if x.type == 'InternalIP'), None)
            gpu = int(node.status.capacity['nvidia.com/gpu']) if 'nvidia.com/gpu' in node.status.capacity else 0
            node_infos.append(NodeInfo(
                labels=labels,
                node_name=labels['kubernetes.io/hostname'],
                gpu=gpu,
                docker_version=node.status.node_info.container_runtime_version,
                kernel_version=node.status.node_info.kernel_version,
                os_image=node.status.node_info.os_image,
                ip=ip_address,
            ))
        return node_infos

    def list_pods_by_node(self, hostname: str) -> List[PodInfo]:
        """
        获取指定节点下的MegaIde Pods信息
        @param hostname: 节点名称
        @return:
        """
        all_pods = self.core_api.list_pod_for_all_namespaces()
        pods = []
        for pod in all_pods.items:
            if pod.spec.node_name == hostname and 'ideType' in pod.metadata.labels:
                pods.append(PodInfo(
                    name=pod.metadata.name,
                    namespace=pod.metadata.namespace,
                    ide_id=pod.metadata.labels['uid'],
                    ip=pod.status.pod_ip,
                    ide_type=pod.metadata.labels['ideType'],
                    startup_time=str(pod.status.start_time)
                ))
        return pods
