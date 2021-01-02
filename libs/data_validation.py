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
        logging.info("ERROR: JSON body data is invalid")
        return False
    
    return True
