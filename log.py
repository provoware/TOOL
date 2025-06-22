import logging, os
from logging.handlers import RotatingFileHandler
LOG_DIR='logs'; os.makedirs(LOG_DIR,exist_ok=True)
handler=RotatingFileHandler(os.path.join(LOG_DIR,'app.log'),maxBytes=1_000_000,backupCount=5,encoding='utf-8')
logging.basicConfig(level=logging.DEBUG,handlers=[handler],format='%(asctime)s | %(levelname)-7s | %(message)s')
log_info=lambda m: logging.info(m)
log_debug=lambda m: logging.debug(m)
def log_error(m,e=None): logging.error(f"{m} | {e}" if e else m)
