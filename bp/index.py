from flask import Blueprint, flash, jsonify, redirect, request, session, url_for

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return { "app_name": "chump", "description": "autodeploy k8s based on flux-gitops principal" }
