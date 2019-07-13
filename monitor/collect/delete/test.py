import time
import logging
from pysnmp.hlapi.asyncore import *
from monitor.collect.setting import Settings
from monitor.collect.db_connect import connect_db
win_oids = [
    # ".1.3.6.1.2.1.25.2.2.0",  # 总内存
    # ".1.3.6.1.2.1.1.5.0",  # 主机名
    ".1.3.6.1.2.1.25.5.1.1.2"
        ]
temp = []
temp1 = []
def add(snmpEngine, sendRequestHandle, errorIndication, errorStatus, errorIndex, varBinds, cbCtx):
    temp.append(varBinds)
    temp1.append(snmpEngine)


def get_info(host, oids):
    # 添加任务
    snmpEngine = SnmpEngine()
    # for host in bmc_setting.hosts:
    for oid in oids:
        getCmd(snmpEngine,
               CommunityData('zhoukun'),  # 1表示V2c
               UdpTransportTarget((host, 161), timeout=3, retries=0, ),  # 传输目标
               ContextData(),
               ObjectType(ObjectIdentity(oid)),
               cbFun=add
               )
    # 执行异步获取snmp
    snmpEngine.transportDispatcher.runDispatcher()
    return temp,temp1


a= get_info("192.168.159.136",win_oids)
print(a)




for i in a:
    print(i)

