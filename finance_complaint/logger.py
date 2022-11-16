import logging
import os
import shutil

from finance_complaint.constant import TIMESTAMP

LOG_DIR = "logs"

def get_log_file_name():
    return f"log_{TIMESTAMP}.log"

LOG_FILE_NAME = get_log_file_name()

if os.path.exists(LOG_DIR):
    shutil.rmtree(LOG_DIR)
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(filename=LOG_FILE_PATH,
                    filemode="w",
                    format='[%(levelname)s \tLineNo: %(lineno)d \tModule: %(filename)s \tFunction: %(funcName)s() \t%(message)s',
                    level=logging.INFO
                    )

logger = logging.getLogger("FinanceComplaint")