from django.shortcuts import render,HttpResponse,redirect
from bmc_admin.models import Host,Host_info
from monitor.models import Monitor
import json
# Create your views here.
def auth(func):
    def inner(request,*args,**kwargs):
        if not request.session.get("is_login", None):
            return redirect("/login")
        return func(request,*args,**kwargs)
    return inner

@auth
def total(request,host_id):
    obj_data = {"x_time":[],
                "cpu":[],
                "memo":[],}
    obj_ip = Host.objects.filter(id=host_id).values()    #根据id查询ip
    host_ip = obj_ip[0]["ip"]
    obj = Monitor.objects.filter(ip_add=host_ip).values()
    mem_total = Host_info.objects.filter(host_ip=host_ip).values("total_memo")[0]["total_memo"]
    count = obj.count()
    data = []
    num, n = 0, 1
    #等距离取出七次
    for i in range(0, count, int(count / 7)):
        data.append(num)
        num += int(count / 7)
        if n == 7:
            break
        n += 1
    for j in data:
        x_time = obj[j]["in_time"]
        cpu = obj[j]["free_cpu_percent"]
        memo = obj[j]["mem_free"]
        obj_data["x_time"].append(str(x_time)[0:16])
        obj_data["cpu"].append(round(100-float(cpu),2))
        obj_data["memo"].append(round(float(memo)/float(mem_total),2))
    obj_data = json.dumps(obj_data)
    return HttpResponse(obj_data)

@auth
def home(request,host_id):
    if request.method == "GET":
        ip = Host.objects.filter(id=host_id).values()[0]["ip"]
        comm = Host.objects.filter(id=host_id).values("community")[0]["community"]
        obj = Host_info.objects.filter(host_ip=ip).values()
    return render(request, "monitor/home.html", {"obj": obj, "comm": comm})


@auth
def memo(request,host_id):
    obj_data = {
            "legend":"内存利用率",
            "times":[],
            "Datas":[],
    }
    obj_ip = Host.objects.filter(id=host_id).values("ip")[0]["ip"]
    mome_total = Host_info.objects.filter(host_ip=obj_ip).values("total_memo")[0]["total_memo"]
    obj = Monitor.objects.filter(ip_add=obj_ip).values("id").all()
    lenght = obj.count()
    obj = obj[lenght - 7:lenght]
    for value in obj:
        times = Monitor.objects.filter(id=value["id"]).values("in_time")[0]["in_time"]
        mem_free = Monitor.objects.filter(id=value["id"]).values("mem_free")[0]["mem_free"]
        per = round(1 - float(mem_free)/float(mome_total),2)
        print(type(per),"ddddd",per)
        obj_data["times"].append(str(times))
        obj_data["Datas"].append(per)
    obj_data = json.dumps(obj_data)
    return HttpResponse(obj_data)

@auth
def total_mem(request,host_id):
    return render(request,"monitor/total_mem.html")

@auth
def cpu_ajax(request,host_id):
    obj_data = {
        "legend": "内存利用率",
        "times": [],
        "Datas": [],
    }
    obj_ip = Host.objects.filter(id=host_id).values("ip")[0]["ip"]
    obj = Monitor.objects.filter(ip_add=obj_ip).values("id").all()
    lenght = obj.count()
    obj = obj[lenght-7:lenght]
    for value in obj:
        times = Monitor.objects.filter(id=value["id"]).values("in_time")[0]["in_time"]
        cpu_free = Monitor.objects.filter(id=value["id"]).values("free_cpu_percent")[0]["free_cpu_percent"]
        per = round(100-float(cpu_free), 2)
        obj_data["times"].append(str(times))
        obj_data["Datas"].append(per)
    obj_data = json.dumps(obj_data)
    return HttpResponse(obj_data)

@auth
def cpu(request,host_id):
    return render(request,"monitor/cpu.html")

@auth
def load_ajax(request,host_id):
    data = {"graph1":[{"value": 0, "name": '1 minute'}],
            "graph2":[{"value": 0, "name": '5 minute'}],
            "graph3":[{"value": 0, "name": '15 minute'}]
            }
    ip = Host.objects.filter(id=host_id).values("ip").first()["ip"]
    min_1 = Monitor.objects.filter(ip_add = ip).values("min_1").order_by("-id").first()["min_1"]
    min_5 = Monitor.objects.filter(ip_add = ip).values("min_5").order_by("-id").first()["min_5"]
    min_15 = Monitor.objects.filter(ip_add = ip).values("min_15").order_by("-id").first()["min_15"]
    data["graph1"][0]["value"] = min_1
    data["graph2"][0]["value"] = min_5
    data["graph3"][0]["value"] = min_15
    data = json.dumps(data)
    return HttpResponse(data)

@auth
def load(request,host_id):
    return render(request,"monitor/load_average.html")
