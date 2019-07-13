from django.shortcuts import render,HttpResponse,redirect
from . import test_snmp
from bmc_admin.models import Host,Host_info
from monitor.models import Monitor
from monitor.collect.setting import Settings
# Create your views here.
bmc_setting = Settings()
def auth(func):
    def inner(request,*args,**kwargs):
        if not request.session.get("is_login", None):
            return redirect("/login")
        return func(request,*args,**kwargs)
    return inner

@auth
def bmc_admin(request):
    if request.method =="POST":
        sys = request.POST.get("system", None)
        ip_add = request.POST.get("ip", None)
        com = request.POST.get("community", None)
        print(sys,ip_add,com)
        if len(sys)==0 or len(ip_add)==0 or len(com)==0:
            return HttpResponse("请输入内容")
        else:
            try:
                Host.objects.create(system=sys,ip=ip_add,community=com)
                #采集设备信息
                value = test_snmp.info_in(ip_add,com,sys)
                if value == None:
                    return HttpResponse("设备信息获取失败！")
                else:
                    name, info_int, num_int ,memo ,cpu= value
                    print("value",value)
                    if sys.lower() == "linux":
                        Host_info.objects.create(host_name=name[0][0:30],
                                                 int_info=" ".join(info_int),
                                                 int_num=num_int[0],
                                                 host_ip=ip_add,
                                                 total_memo=memo[0],
                                                 cpu_info = cpu[0][0:70] )
                    elif sys.lower() == "windows":
                        x= "".join(info_int)
                        z = x.split("0x")
                        y = "".join(z)
                        info_int = bytearray.fromhex(y).decode()
                        print(info_int,len(info_int))
                        Host_info.objects.create(host_name=name[0][0:30],
                                                 int_info=info_int,
                                                 int_num=num_int[0],
                                                 host_ip=ip_add,
                                                 total_memo=memo[0],
                                                 cpu_info=cpu[0][0:70])
            except Exception as e:
                return HttpResponse(e)
        return HttpResponse("添加成功")
    host_obj = Host.objects.all()
    return render(request, "bmc_admin/bmc_admin.html",{"host_obj":host_obj,
                                                       "count":host_obj.count()
                                                       })
@auth
def snmp_test(request):
    if request.method =="POST":
        sys = request.POST.get("system", None)
        ip_add = request.POST.get("ip", None)
        com = request.POST.get("community", None)
        if len(sys) == 0 or len(ip_add) == 0 or len(com) == 0:
            return HttpResponse("请输入内容")
        else:
            s = test_snmp.test(ip_add,com)
            return HttpResponse(s)
    return render(request, "bmc_admin/snmp_test.html")


@auth
def delete(request,nid):
    ip = Host.objects.filter(id=nid).values("ip")[0]["ip"]
    Host.objects.filter(id=nid).delete()
    Host_info.objects.filter(host_ip=ip).delete()
    Monitor.objects.filter(ip_add=ip).delete()
    return redirect("/bmc_admin")