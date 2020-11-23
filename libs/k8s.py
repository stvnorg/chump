import json
from kubernetes import client, config

class K8s:
    def __init__(self, namespace, deployment_name, container_name):
        config.load_kube_config()
        self.v1 = client.AppsV1Api()
        self.namespace = namespace
        self.deployment_name = deployment_name
        self.container_name = container_name

    def check_image_update(self, image_version):
        self.ret = self.v1.read_namespaced_deployment(self.deployment_name, self.namespace)
        self.deployment_metadata = json.loads(self.ret.metadata.annotations['kubectl.kubernetes.io/last-applied-configuration'])

        for deployment in self.deployment_metadata['spec']['template']['spec']['containers']:
            if deployment['name'] == self.container_name and deployment['image'] == image_version:
                return False

        return True

    def __str__(self):
        return "k8s class to check the current deployment"
