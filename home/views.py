from django.shortcuts import render,HttpResponse,redirect
from bmc_admin import models as bmc
from monitor import models as mon
from . import percent
import json

# Create your views here.

def auth(func):
    def inner(request,*args,**kwargs):
        if not request.session.get("is_login", None):
            return redirect("/login")
        return func(request,*args,**kwargs)
    return inner

@auth
def index(request):
    if request.method == "GET":
        obj = bmc.Host.objects.all()
    return render(request, "home/index.html", {"obj": obj})



def graph3(request):
    obj = bmc.Host.objects.all()
    obj_data = {"legend":[],
                "data":[],
                }
    name = obj.values("system").distinct()
    count = 0
    for k in name:
        obj_data["data"].append({})
        sys_name = k["system"]
        obj_data["legend"].append(sys_name)
        a = obj.filter(system=sys_name).count()
        obj_data["data"][count]["value"]= a
        obj_data["data"][count]["name"]= sys_name
        count += 1

    obj_data= json.dumps(obj_data)
    return HttpResponse(obj_data)

def graph2(request):
    obj = mon.Monitor.objects.all()
    obj2 = bmc.Host_info.objects.all()
    a = obj.values("ip_add").distinct()
    free_memo = []
    total_memo = []
    for k in a:
        host = k["ip_add"]
        memo_total = obj2.filter(host_ip=host).values("total_memo").first()
        memo_total = memo_total["total_memo"]
        memo = obj.filter(ip_add=host).values("mem_free").order_by("-id").first()
        memo = memo["mem_free"]
        if memo == None:
            free_memo.append("0")
            total_memo.append("0")
            continue
        else:
            total_memo.append(memo_total)
            free_memo.append(memo)
    obj_data = percent.memo_percent(free_memo, total_memo)
    obj_data = json.dumps(obj_data)
    return HttpResponse(obj_data)

def graph1(request):
    obj = mon.Monitor.objects.all()
    a = obj.values("ip_add").distinct()
    free_cpu = []
    for k in a:
        host = k["ip_add"]
        free = obj.filter(ip_add=host).values("free_cpu_percent").order_by("-id").first()
        free = free["free_cpu_percent"]
        if free == None:
            free_cpu.append("0")
            continue
        else:
            free_cpu.append(free)
    obj_data = percent.cpu_percent(free_cpu)
    obj_data = json.dumps(obj_data)
    return HttpResponse(obj_data)
