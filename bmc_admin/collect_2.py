from pysnmp.entity.rfc3413.oneliner import cmdgen
from monitor.collect.setting import Settings
bmc_admin = Settings()
class GetSnmp():
    #oid列表
    def make_list(self,*oid):
        oid_list = []
        for o in oid:
            oid_list.append(o)
        return oid_list
    #获取snmp信息
    def info(self,oid,ip,commu):
        # pass
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.CommunityData(commu),
            cmdgen.UdpTransportTarget((ip, 161)),
            oid,
        )
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1][0] or '?'
                    )
                )
            else:
                var_dict=[]
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        var_dict.append(str(val.prettyPrint()))
                return var_dict

    #循环oid表，提取整理信息
    def get_info(self,oid,ip,commu='zhoukun'):
        info_dict={}
        for o in oid:
            info = self.info(o,ip,commu)
            info_dict[o]=info
        # print(info_dict)
        return info_dict

