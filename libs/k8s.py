import json
from kubernetes import client, config

class K8s:
    def __init__(self):
        config.load_kube_config()
        self.v1 = client.AppsV1Api()

    def kustomize_deploy(self, namespace, deployment_name, image_name):
        self.ret = self.v1.read_namespaced_deployment(deployment_name, namespace)
        self.deployment_metadata = json.loads(self.ret.metadata.annotations['kubectl.kubernetes.io/last-applied-configuration'])

        for deployment in self.deployment_metadata['spec']['template']['spec']['containers']:
            if deployment['image'] == image_name:
                print(image_name)

    def __str__(self):
        return "k8s function to check the current deployment"
