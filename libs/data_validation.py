from .app_logging import use_logging

logging = use_logging()

def json_data_is_valid(data):
    try:
        if not data['namespace']: 
            return False
        if not data['deployment_name']: 
            return False
        if not data['git_url']: 
            return False
        if not data['branch']: 
            return False
        if not data['deploy_path']: 
            return False
        if not data['container_name']: 
            return False
        if not data['image_version_file']: 
            return False
    except Exception as e:
        return False
    
    return True

def source_already_exist(source, source_data):
    try:
        if source['namespace'] != source_data['namespace']:
            return False
        if source['deployment_name'] != source_data['deployment_name']:
            return False
        if source['git_url'] != source_data['git_url']:
            return False
        if source['branch'] != source_data['branch']:
            return False
        if source['deploy_path'] != source_data['deploy_path']:
            return False
        if source['container_name'] != source_data['container_name']:
            return False
        if source['image_version_file'] != source_data['image_version_file']:
            return False
    except Exception as e:
        return False
    
    return True