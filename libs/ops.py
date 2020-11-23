import os
import yaml
from subprocess import run

class Ops:
    def __init__(self, logging, k8s, git_url, branch, deploy_path, container_name, image_version_file):
        self.logging = logging
        self.k8s = k8s
        self.git_url = git_url
        self.branch = branch
        self.deploy_path = deploy_path
        self.container_name = container_name
        self.image_version_file = image_version_file

    def get_image_version(self, container_name, image_version_file):
        with open(image_version_file, 'r') as f:
            yaml_data = yaml.load_all(f, Loader=yaml.FullLoader)
            for data in yaml_data:
                for key, value in data.items():
                    try:
                        containers = value['template']['spec']['containers']
                        for container in containers:
                            if container['name'] == container_name:
                                return container['image']
                    except:
                        pass

    def clone_and_deploy(self):
        try:
            root_dir = os.getcwd()
            args = ["git", "clone", self.git_url]
            run(args, check=True)

            working_dir = self.git_url.split('/')[::-1][0]
            working_dir = working_dir.split('.')[0]

            os.chdir(working_dir)

            args = ["git", "checkout", self.branch]
            self.logging.info(run(args, check=True))

            self.logging.info(self.k8s)

            self.image_version = self.get_image_version(self.container_name, self.image_version_file)
            self.logging.info(self.image_version)

            if self.k8s.check_image_update(self.image_version):
                args = "kustomize build {} | kubectl apply -f -".format(self.deploy_path)
                self.logging.info(args)
                self.logging.info(os.system(args))
            else:
                self.logging.info("No new update!")

            os.chdir(root_dir)
            args = ["rm", "-rf", os.path.join(root_dir, working_dir)]
            self.logging.info(run(args, check=True))

        except Exception as exception_msg:
            raise exception_msg
