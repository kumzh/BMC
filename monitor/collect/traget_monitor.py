from monitor.collect.db_connect import connect_db
from monitor.collect.email import EmailHandler
from monitor.collect.setting import Settings
import time
bmc_admin = Settings()
db,cur = connect_db()

def mess_push(hostid,value,bmc_setting):
    print(len(bmc_setting.to_mail_info))
    if len(bmc_setting.to_mail_info) ==0:
        bmc_setting.time = time.time()
    else:
        num = int(time.time()) - int(bmc_setting.time)
        print("num",num)
        email = EmailHandler(bmc_setting.from_mail_info[0][0], bmc_setting.from_mail_info[0][1])
        for i in range(len(bmc_setting.target_info)):
            target = bmc_setting.target_info[i][0]
            target_value = bmc_setting.target_info[i][1]
            if target == "CPU":
                # memfree = value[0]
                freecpupercent = value[1]
                a = 100 - int(freecpupercent)
                if int(target_value) < a and (num > 600 or num < 15):
                    print("告警")
                    email.send_mail(bmc_setting.to_mail_info[0][0],
                                    "CPU告警",
                                    "主机%s CPU利用率超出阈值"%hostid)
                    bmc_setting.time = int(time.time()) - 15
                elif int(target_value) < a and not (num > 600 or num < 15):
                    pass
                elif int(target_value) > a:    #告警消失
                    bmc_setting.time = time.time()
                else:
                    pass





        # elif target == "memo":
        #     memfree, freecpupercent, usetime, system = value