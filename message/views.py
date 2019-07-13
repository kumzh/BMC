from django.shortcuts import render,HttpResponse,redirect
from .models import From_mail,To_mail,Target
from .email import EmailHandler
import smtplib,re

# Create your views here.

def auth(func):
    def inner(request,*args,**kwargs):
        if not request.session.get("is_login", None):
            return redirect("/login")
        return func(request,*args,**kwargs)
    return inner


def mail_auth(from_add,passwd):
    add_server = from_add.split("@")[-1]
    if "163" in add_server:
        server = "smtp."+add_server
    else:
        return "邮箱不支持"
    try:
        smtpobj = smtplib.SMTP(server,25)
        t = smtpobj.login(from_add,passwd)
    except Exception as e:
        print("error",e)
        return "验证失败"
    return "验证通过"

@auth
def mesg(request):
    if request.method == "POST":
        from_add = request.POST.get("from_add", None)
        password = request.POST.get("from_passwd", None)
        if len(from_add) == 0 or len(password) == 0:
            return HttpResponse("请输入内容")
        From_mail.objects.create(form_mail_add=from_add, passwd=password)
        return HttpResponse("添加成功")
    from_mail_obj = From_mail.objects.all()
    return render(request, "message/mesg.html", {"from_obj": from_mail_obj,
                                                 "count": from_mail_obj.count(),
                                                 })


@auth
def mail_test(request):
    if request.method == "POST":
        from_add = request.POST.get("from_add", None)
        passwd = request.POST.get("from_passwd", None)
        if len(from_add) == 0 or len(passwd) == 0:
            return HttpResponse("请输入内容")
        dec = mail_auth(from_add, passwd)
        return HttpResponse(dec)
    return render(request, "message/mesg.html")



def to_mail_auth(from_add,passwd,to_add):
    mail = EmailHandler(from_add, passwd, 1)
    dec = mail.send_mail(to_add, "测试邮件", "这是一封监控平台测试邮件，请勿回复")
    return dec

@auth
def to_mail_add(request):
    if request.method == "POST":
        to_add = request.POST.get("to_add", None)
        if len(to_add) == 0:
            return HttpResponse("请输入内容")
        elif re.match(r'[0-9a-zA-Z_]{0,19}@[0-9A-Za-z]{0,10}.com', to_add):
            To_mail.objects.create(to_mail=to_add)
            dec = '添加成功！'
        else:
            dec = '邮箱格式错误'
        return HttpResponse(dec)
    to_mail_obj = To_mail.objects.all()
    return render(request, "message/to_mail_add.html", {"to_obj": to_mail_obj,
                                                        "count": to_mail_obj.count()
                                                        })

@auth
def to_mail_test(request):
        if request.method == "POST":
            to_add = request.POST.get("to_add",None)
            if len(to_add)==0 :
                return HttpResponse("请输入内容")
            elif re.match(r'[0-9a-zA-Z_]{0,19}@[0-9A-Za-z]{0,10}.com', to_add):
                obj = From_mail.objects.values().first()
                from_add = obj["form_mail_add"]
                passwd = obj["passwd"]
                dec = to_mail_auth(from_add,passwd,to_add)
            else:
                dec = '邮箱格式错误'
            return HttpResponse(dec)
        return render(request,"message/to_mail_add.html")

@auth
def target_set(request):
    if request.method == "POST":
        target_in = request.POST.get("target", None)
        value_in = request.POST.get("value", None)
        if len(target_in) == 0 or len(value_in) == 0:
            return HttpResponse("请输入内容")
        else:
            Target.objects.create(target=target_in, value=value_in)
            return HttpResponse("添加成功")
    target_obj = Target.objects.all()
    return render(request, "message/target_set.html", {"target": target_obj,
                                                       "count": target_obj.count(),
                                                       })



@auth
def from_delete(request,nid):
    From_mail.objects.filter(id=nid).delete()
    return redirect("/mail")


@auth
def to_delete(request,nid):
    To_mail.objects.filter(id=nid).delete()
    return redirect("/mail/to_mail_add")


@auth
def target_delete(request,nid):
    Target.objects.filter(id=nid).delete()
    return redirect("/mail/target_set")


