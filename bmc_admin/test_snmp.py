from bmc_admin.collect_2 import GetSnmp
from . import setting
bmc_admin = setting.Settings()
def test(ip,community):
    oids =["1.3.6.1.2.1.1.1"]
    # monitor = collet_main.Monitor()
    monitor = GetSnmp()
    myq = monitor.get_info(oids,ip,community)
    # status = myq.get(block=False)
    # print("statue",status)
    if len(myq["1.3.6.1.2.1.1.1"]) !=0:
        return "snmp正常"
    elif len(myq["1.3.6.1.2.1.1.1"])== 0:
        return "snmp 连接错误"

def info_in(ip,community,sys):
    if sys.lower() == "linux":
        oids = bmc_admin.hw_info
    elif sys.lower() == "windows":
        oids = bmc_admin.win_hw_info
    monitor = GetSnmp()
    info = monitor.get_info(oids,ip,community)
    value = list(info.values())
    if [""] in value:
        return None
    else:
        return value

# v = test("192.168.159.134","zhoukun")
# # name, info_int, num_int ,memo ,cpu= v
# print("v",v)