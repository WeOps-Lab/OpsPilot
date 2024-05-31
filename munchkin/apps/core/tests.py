from apps.core.utils.kubernetes_client import KubernetesClient


def test_train_pilot():
    client = KubernetesClient("argo")
    client.train_pilot("1")
