#!/usr/bin/env python3

import logging
import json
import os
import socket
import threading
from subprocess import run
from time import sleep

LOGGING_FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO,
                        datefmt="%H:%M:%S")

git_sources = os.path.join(os.getcwd(), "git-sources.json")

def clone_and_deploy(git_url, branch, deploy_path):
    try:
        args = ["git", "clone", git_url]
        run(args, check=True)

        working_dir = git_url.split('/')[::-1][0]
        working_dir = working_dir.split('.')[0]

        os.chdir(working_dir)

        args = ["git", "checkout", branch]
        run(args, check=True)

        args = ["cat", deploy_path]
        run(args, check=True)

        args = ["kustomize", "build", deploy_path, "|", "kubectl", "apply", "-f", "-"]
        run(args)

        args = ["rm", "-rf", os.path.join(os.getcwd(), working_dir)]
        run(args, check=True)

    except Exception as exception_msg:
        raise exception_msg

def check_code_update():
    while True:
        with open(git_sources, 'r') as file:
            sources = json.load(file)['git-sources']
            for source in sources:
                git_url = source['git_url']
                branch = source['branch']
                deploy_path = source['deploy_path']
                clone_and_deploy(git_url, branch, deploy_path)
        sleep(60)
    return 0

def api_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 9999))
    server.listen(5)

    while True:
        conn, addr = server.accept()
        from_client = ''
        while True:
            data = conn.recv(4096).decode()
            if not data:
                break
            from_client += data
            logging.info("Data from client: {}".format(from_client))
            conn.send(b'I am SERVER<br>')
        conn.close()
        logging.info('client disconnected')

if __name__ == "__main__":
    check_git_status = threading.Thread(target=check_code_update)
    listen_to_client = threading.Thread(target=api_server)

    check_git_status.start()
    listen_to_client.start()
