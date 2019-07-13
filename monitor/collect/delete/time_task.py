#python3
import os,sys,time
from monitor.collect.delete.server_monitor import monitor_main
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

def roll_polling(cmd,hostid,community,sec = 60):
    while True:
        #TODO task
        monitor_main(hostid,community)
        time.sleep(sec)

