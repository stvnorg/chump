#!/usr/bin/env python3

import json
import logging
import os
import threading
from time import sleep
from libs.k8s import K8s
from libs.ops import Ops
from libs.db import db_setup, create_table, get_git_sources
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import Flask
from bp import api, index

app = Flask(__name__)

app.register_blueprint(api.bp)
app.register_blueprint(index.bp)

LOGGING_FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO,
                        datefmt="%Y-%m-%d %H:%M:%S")

DELAY_TIME = 60
git_sources = os.path.join(os.getcwd(), "git-sources.json")

def check_code_update():
    while True:
        with open(git_sources, 'r') as file:
            sources = get_git_sources()
            for source in sources:
                namespace = source['namespace']
                deployment_name = source['deployment_name']
                git_url = source['git_url']
                branch = source['branch']
                deploy_path = source['deploy_path']
                container_name = source['container_name']
                image_version_file = source['image_version_file']

                k8s = K8s(namespace, deployment_name, container_name)
                ops = Ops(k8s, git_url, branch, deploy_path, container_name, image_version_file)
                ops.clone_and_deploy()
        sleep(DELAY_TIME)
    return app

def run_app():
    db_setup()
    create_table()
    check_code_update()

check_git_status = threading.Thread(target=run_app)
check_git_status.start()
