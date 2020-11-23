import os
from subprocess import run

class Ops:
    def __init__(self, logging, k8s):
        self.logging = logging
        self.k8s = k8s

    def clone_and_deploy(self, git_url, branch, deploy_path):
        try:
            root_dir = os.getcwd()
            args = ["git", "clone", git_url]
            run(args, check=True)

            working_dir = git_url.split('/')[::-1][0]
            working_dir = working_dir.split('.')[0]

            os.chdir(working_dir)

            args = ["git", "checkout", branch]
            self.logging.info(run(args, check=True))

            print(self.k8s)

            args = "kustomize build {} | kubectl apply -f -".format(deploy_path)
            self.logging.info(args)
            #self.logging.info(os.system(args))

            os.chdir(root_dir)
            args = ["rm", "-rf", os.path.join(os.getcwd(), working_dir)]
            self.logging.info(run(args, check=True))

        except Exception as exception_msg:
            raise exception_msg
