#!/usr/bin/env python3

import argparse
import json
import logging
from multiprocessing import Process
import os
import socket
import threading
from time import sleep
from libs.k8s import K8s
from libs.ops import Ops
from libs.db import DBSetup, CreateTable
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import Flask, g

app = Flask(__name__)

LOGGING_FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO,
                        datefmt="%Y-%m-%d %H:%M:%S")

DELAY_TIME = 60
git_sources = os.path.join(os.getcwd(), "git-sources.json")

def check_code_update(g):
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
                ops = Ops(k8s, git_url, branch, deploy_path, container_name, image_version_file)
                ops.clone_and_deploy()
        sleep(DELAY_TIME)
    return app

def db_setup(g):
    with app.app_context():
        g.logging = logging
        DBSetup()
        CreateTable()
    return app

def run_app():
    with app.app_context():
        g.logging = logging
        check_code_update(g)

check_git_status = threading.Thread(target=run_app)
check_git_status.start()

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--setup', dest='run_setup', action='store_true')

    args = parser.parse_args()
    if args.run_setup:
        db_setup(g)
