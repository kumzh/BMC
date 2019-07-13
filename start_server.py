from monitor.collect.delete.thread import create_thread

import os
import logging
logging.basicConfig(filename='collect_log.txt',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
if __name__ == "__main__":
    logging.info("collect start")
    create_thread()
    str = "python manage.py runserver"
    os.system(str)
