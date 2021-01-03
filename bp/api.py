from libs.db import add_git_source, delete_git_source, get_git_sources
from libs.custom_msg import custom_msg_dict, custom_response_msg
from libs.data_validation import json_data_is_valid
from flask import Blueprint, flash, jsonify, redirect, request, session, url_for
from werkzeug.exceptions import abort

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/', methods=['GET'])
def api():
    return { "endpoints" : ["api/health", "api/sources"] }

@bp.route('/health/', methods=['GET'])
def health():
    return { "status" : "healthy" }

@bp.route('/sources/', methods=['GET'])
def sources():
    return { "sources": get_git_sources() }

@bp.route('/sources/<int:source_id>/', methods=['GET'])
def retrieve(source_id):
    return get_git_sources(source_id)

@bp.route('/sources/create', methods=['POST'])
def create():
    if request.is_json:
        try:
            req = request.get_json()
            if json_data_is_valid(req):
                return add_git_source(req)
            else:
                msg = "JSON body data is invalid"
                return custom_response_msg(msg, 200)

        except Exception as e:
            print(e)
            msg = "Internal server error"
            return custom_response_msg(msg, 500)
    else:
        msg = "Request body must be JSON data"
        return custom_response_msg(msg, 400)

@bp.route('/sources/<int:source_id>/update', methods=['PUT', 'PATCH'])
def update(source_id):
    return 'update'

@bp.route('/sources/<int:source_id>/delete', methods=['DELETE'])
def delete(source_id):
    return delete_git_source(source_id)
    