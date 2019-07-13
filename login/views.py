from django.shortcuts import render,redirect,HttpResponse
from .models import LoginUser
# Create your views here.

def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        rem = request.POST.get("remember")
        temp = LoginUser.objects.filter(username=user).values('userpasswd')
        if len(temp) == 0:
            return render(request, "login/login.html",{"mes":"用户名或者密码不正确！"})
        else:
            userpasswd = temp[0]["userpasswd"]
            if pwd == userpasswd:
                request.session["username"] = user
                request.session["is_login"] = True
                if  rem == "true":
                    request.session.set_expiry(60 * 30)   #设置六十秒超时
                else:
                    request.session.set_expiry(60 * 5)
                return redirect("/")
            else:
                return render(request,"login/login.html",{"mes":"用户名或者密码不正确！"})
    return render(request, "login/login.html", {"mes": ''})



def logout(request):
    if request.method == "POST":
        request.session.clear()  # 注销
    return redirect("/login")