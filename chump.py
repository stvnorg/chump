#!/usr/bin/env python3

import logging
import json
import os
import socket
import threading
from time import sleep
from libs.k8s import *
from libs.ops import *
from flask import Flask
app = Flask(__name__)

LOGGING_FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO,
                        datefmt="%Y-%m-%d %H:%M:%S")

git_sources = os.path.join(os.getcwd(), "git-sources.json")
delay_time = 60

def check_code_update():
    while True:
        with open(git_sources, 'r') as file:
            sources = json.load(file)['git-sources']

            for source in sources:
                namespace = source['namespace']
                deployment_name = source['deployment_name']
                git_url = source['git_url']
                branch = source['branch']
                deploy_path = source['deploy_path']
                container_name = source['container_name']
                image_version_file = source['image_version_file']

                k8s = K8s(namespace, deployment_name, container_name)
                ops = Ops(logging, k8s, git_url, branch, deploy_path, container_name, image_version_file)
                ops.clone_and_deploy()
        sleep(delay_time)
    return 0

check_git_status = threading.Thread(target=check_code_update)
check_git_status.start()

@app.route('/')
def hello_world():
    return 'Hello, World!'

