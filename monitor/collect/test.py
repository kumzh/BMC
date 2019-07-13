import threading
import threading,logging
import os,sys
import time
from monitor.collect.setting import Settings
from monitor.collect.db_connect import connect_db
from pysnmp.hlapi.asyncore import *
import queue
import operator
logging.basicConfig(filename='collect_log.txt',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

db,cur = connect_db()
bmc_setting = Settings()

class Job(threading.Thread):
    def __init__(self,hostid,system,community,sec):
        super(Job, self).__init__()
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True
        self.hostid = hostid
        self.system = system
        self.community = community
        self.sec = sec
    def run(self):
        print("running %s" % self.__running.isSet())
        while self.__running.isSet():
            # self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            thread_obj = threading.current_thread()
            monit = Monitor()
            print(self.hostid)
            oids = sel_oids(self.system)
            print("oid init %s" % oids)
            if oids == None:
                value = None
                print("adjust ")
            else:
                myq = monit.get_info(self.hostid, oids, self.community)
                print("myq %s" % myq)
                value = monit.change(myq, oids)
                print("vale %s" % value)
            if value == None:
                print("%s snmp none" % thread_obj)
                print("exit", threading.activeCount())
                if threading.activeCount() == 1:
                    sys.exit()
            else:
                print("%s not none" % thread_obj)
                data_in(self.hostid, value)
            time.sleep(5)
    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞
    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞
    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False


class Monitor():
    def __init__(self):
        self.f_data = []
        self.myq = queue.Queue()
    # 回调函数。在有数据返回时触发
    def add(self, snmpEngine, sendRequestHandle, errorIndication, errorStatus, errorIndex, varBinds, cbCtx):
        self.myq.put(varBinds)
    def get_info(self, host, oids, community):
        # 添加任务
        snmpEngine = SnmpEngine()
        for oid in oids:
            getCmd(snmpEngine,
                   CommunityData(community),  # 1表示V2c
                   UdpTransportTarget((host, 161), timeout=3, retries=0, ),  # 传输目标
                   ContextData(),
                   ObjectType(ObjectIdentity(oid)),
                   cbFun=self.add
                   )
        # 执行异步获取snmp
        snmpEngine.transportDispatcher.runDispatcher()
        return self.myq

    def change(self,myq,oids):
        oid_temp = []
        while True:
            try:
                info = myq.get(block=False)
                if len(info) == 0:
                    break
                else:
                    per_oid = info[0][0]
                    oid_temp.append(str(per_oid))
                    per_info = info[0][1]
                    self.f_data.append(str(per_info))
            except queue.Empty:
                break
        if operator.ne(oids,oid_temp):
            return None
        else:
            return self.f_data

def data_in(hostid, value):
    memfree, freecpupercent, usetime, system = value
    seconds = int(usetime)/100
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    usetime = str("%02d:%02d:%02d" % (h, m, s))
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    insert_sql = """insert into monitor_monitor(ip_add, mem_free, free_cpu_percent, use_time,in_time) 
                                            values(%s, %s, %s, %s, %s)"""
    cur.execute(insert_sql, (hostid,  memfree, freecpupercent, usetime, time_now))
    db.commit()

#根据系统查询OID
def sel_oids(system):
    if system.lower() == "linux":
        return bmc_setting.linux_oids
    elif system.lower() == "windows":
        return None
    else:
        logging.error("Devices are not supported!")
        return None

#将host信息提取出来存放到全局变量中
def select():
    select_sql = """select ip,system,community from bmc_admin_host"""
    cur.execute(select_sql)
    results = cur.fetchall()
    results = list(results)
    bmc_setting.host_info = results

#创建线程
def create_thread():
    while True:
        select()
        print("host_info ",bmc_setting.host_info)
        for i in range(len(bmc_setting.host_info)):
            host_id = bmc_setting.host_info[i][0]
            community = bmc_setting.host_info[i][2]
            system = bmc_setting.host_info[i][1]
            thread = Job(host_id,system,community,5)
            bmc_setting.thread_status.append(thread)
            logging.info("create thread")
            thread.start()
        for i in bmc_setting.thread_status:
            i.stop()
        time.sleep(60)



if __name__ == "__main__":
    logging.info("collect start")
    print("first",bmc_setting.thread_status)
    create_thread()
