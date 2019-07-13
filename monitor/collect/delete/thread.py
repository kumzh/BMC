import threading,logging
from monitor.collect.setting import Settings
from monitor.collect.delete.time_task import roll_polling
from monitor.collect.db_connect import connect_db
logging.basicConfig(filename='collect_log.txt',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
db,cur = connect_db()


def select():
    select_sql = """select ip,system,community from bmc_admin_host"""
    cur.execute(select_sql)
    results = cur.fetchall()
    print(list(results))
    print(len(results))
    return results


bmc_setting = Settings()
#需要线程锁，不然一个线程崩了影响其他进程
def create_thread():
    hosts = select()
    for i in range(len(hosts)):
        thread = threading.Thread(target=roll_polling,args=("echo %time%",hosts[i][1],hosts[i][2],bmc_setting.collect_time))
        logging.info("create thread")
        thread.start()



