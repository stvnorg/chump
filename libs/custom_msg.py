from .app_logging import use_logging

logging = use_logging()

custom_msg_dict = { 
    "add_source_success": "[INFO] Add new source success!",
    "add_source_failed": "[INFO] Add new source failed!",
    "delete_source_success": "[INFO] Source has been deleted!",
    "delete_source_failed": "[ERROR] Deleting source failed!",
    "duplicated_source": "[WARN] Source already exist!",
    "source_doesnt_exist": "[WARN] Source doesn't exist!",
    "update_source_success": "[INFO] Source has been updated!",
    "update_source_failed": "[ERROR] Updating source failed!"
 }

def custom_response_msg(msg, http_status_code):
    logging.info(msg)
    return { "msg": msg }, http_status_code