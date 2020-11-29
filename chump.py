#!/usr/bin/env python3

import json
import logging
import os
import threading
from time import sleep
from libs.k8s import K8s
from libs.ops import Ops
from libs.db import DBSetup, CreateTable, GetGitSources
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import Flask, g

app = Flask(__name__)

LOGGING_FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO,
                        datefmt="%Y-%m-%d %H:%M:%S")

DELAY_TIME = 60
git_sources = os.path.join(os.getcwd(), "git-sources.json")

def db_setup(g):
    with app.app_context():
        g.logging = logging
        DBSetup()
        CreateTable()
    return app

def db_should_exist(func):
    def wrapper():
        try:
            logging.info("Make sure the DB exist...")
            db_setup(g)
            func()
        except Exception as e:
            logging.info(e)
            logging.info("Failed to create DB!")
    return wrapper

def check_code_update(g):
    while True:
        with open(git_sources, 'r') as file:
            GetGitSources()
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

@db_should_exist
def run_app():
    with app.app_context():
        g.logging = logging
        check_code_update(g)

check_git_status = threading.Thread(target=run_app)
check_git_status.start()

@app.route('/')
def hello_world():
    return 'Hello, World!'
