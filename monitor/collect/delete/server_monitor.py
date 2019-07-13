import time
import logging
from pysnmp.hlapi.asyncore import *
from monitor.collect.setting import Settings
from monitor.collect.db_connect import connect_db
logging.basicConfig(filename='collect_log.txt',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

bmc_setting = Settings()
db,cur = connect_db()

class Monitor():
    def __init__(self):
        self.temp = []   #接收采集数据
        self.b = []    #

    # 回调函数。在有数据返回时触发
    def add(self,snmpEngine, sendRequestHandle, errorIndication, errorStatus, errorIndex, varBinds, cbCtx):
        self.temp.append(varBinds)
    def get_info(self,host,oids,community):
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
        return self.temp

    def change(self,data_obj):
        for i in data_obj:
            c = i[0][1]    #获取对象中的数据
            if type(c).__name__ == "DisplayString":
                c = str(c).split()[0]
                self.b.append(c)
                continue
            self.b.append(str(c))
        return self.b


def data_in(hostid,value):
    n = 1024 * 1024
    memtotal, memfree, freecpupercent, usetime, system = value
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    insert_sql = """insert into monitor_monitor(ip_add,mem_total, mem_free, free_cpu_percent, use_time,in_time) 
                                            values(%s, %s, %s, %s, %s, %s)"""
    cur.execute(insert_sql, (hostid, memtotal, memfree, freecpupercent, usetime,time_now))
    db.commit()

def sel_oids(system):
    if system.lower() == "linux":
        return bmc_setting.linux_oids
    elif system.lower() == "windows":
        pass
    else:
        logging.error("Devices are not supported!")
        return 0


def monitor_main(host_id,system,community):
    try:
        monit = Monitor()
        print(host_id)
        oids = sel_oids(system)
        a = monit.get_info(host_id,oids,community)
        value = monit.change(a)

        data_in(host_id, value)
    except Exception as e:
        logging.error("snmp error")
        print(e)





