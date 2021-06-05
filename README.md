# Chump Repository

Auto deploy kubernetes using kustomize based on flux gitops. You need to have a valid kustomize k8s deployment files inside the repo.

## Requirements:
- Python v3.5.x or above
- RethinkDB (docker or standalone)
- Kustomize
- Make sure that the chump application has access to the k8s cluster to run the deployment

## Introduction

It has 2 components REST-API and Threading python process. 

The threading process:
- Query the list of git-sources from the RethinkDB
- Git clone the target repository.
- Check the latest image version of a k8s deployment and compare the current running version with the kustomize image version in the repository. 
- If the image version is different, it will run the deployment ```kustomize build . | kubectl apply -f -```

REST-API:

A simple CRUD (Create, Retrieve, Update, Delete) API to add, query, update and delete a git-source.


## Git sources format
```bash
{
    "namespace": "production",
    "deployment_name": "helloworld",
    "git_url": "https://github.com/stvnorg/helloworld.git",
    "branch": "master",
    "deploy_path": "./deploy/helloworld/deployment.yaml",
    "container_name": "helloworld",
    "image_version_file": "./deploy/helloworld/deployment.yaml"
}
```

## Installation

1. Install kustomize (https://kubectl.docs.kubernetes.io/installation/kustomize/)

2. Install RethinkDB (https://rethinkdb.com/docs/install/)

3. Install chump

```bash
$ git clone https://github.com/stvnorg/chump
$ cd chump
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ gunicorn chump:app
```
gunicorn will start both API and Threading process

For changing the API port, bind to specific IP Address and the worker size you can refer to https://docs.gunicorn.org/en/latest/settings.html?highlight=port#bind

## Usage

#### Create new git source
```bash
curl -X POST -H "Content-Type: application/json" http://CHUMP_URL/api/sources/create -d '{"namespace": "<NAMESPACE>", "deployment_name": "<DEPLOYMENT_NAME>", "git_url": "<GIT_URL>", "branch": "<GIT_BRANCH>", "deploy_path": "<KUSTOMIZE_DEPLOY_PATH>", "container_name": "<CONTAINER_NAME>", "image_version_file": "<KUSTOMIZE_FILE_WHERE_THE_IMAGE_VERSION_DECLARED"}'
```
example:
```bash
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/api/sources/create -d '{"namespace": "production", "deployment_name": "helloworld", "git_url": "https://github.com/stvnorg/helloworld.git", "branch": "master", "deploy_path": "./deploy/helloworld/deployment.yaml", "container_name": "helloworld", "image_version_file": "./deploy/helloworld/deployment.yaml"}'
```

#### Retrieve (query) git sources
1. Query for all data
```bash
curl -X GET http://CHUMP_URL/api/sources
```

2. Query for specific id
```bash
curl -X GET http://CHUMP_URL/api/sources/<GIT_SOURCE_ID:integer>
```
example:
```bash
curl -X GET http://CHUMP_URL/api/sources/1
```

#### Update a git source
```bash
curl -i -X PATCH -H "Content-Type: application/json" http://CHUMP_URL/api/sources/<GIT_SOURCE_ID:integer>/update -d '{"namespace": "<NAMESPACE>", "deployment_name": "<DEPLOYMENT_NAME>", "git_url": "<GIT_URL>", "branch": "<GIT_BRANCH>", "deploy_path": "<KUSTOMIZE_DEPLOY_PATH>", "container_name": "<CONTAINER_NAME>", "image_version_file": "<KUSTOMIZE_FILE_WHERE_THE_IMAGE_VERSION_DECLARED"}'
```

example:
```bash
curl -i -X PATCH -H "Content-Type: application/json" http://127.0.0.1:8000/api/sources/1/update -d '{"namespace": "production", "deployment_name": "helloworld", "git_url": "https://github.com/stvnorg/helloworld.git", "branch": "master", "deploy_path": "./deploy/helloworld/deployment.yaml", "container_name": "helloworld-container", "image_version_file": "./deploy/helloworld/deployment.yaml"}'
```

#### Delete a git source
```bash
curl -i -X DELETE http://CHUMP_URL/api/sources/<GIT_SOURCE_ID:integer>/delete
```
example
```bash
curl -i -X DELETE http://127.0.0.1:8000/api/sources/1/delete
```

