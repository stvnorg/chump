from .app_logging import use_logging

logging = use_logging()

def custom_response_msg(msg, http_status_code):
    logging.info(msg)
    return { "msg": msg }, http_status_code