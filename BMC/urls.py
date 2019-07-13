"""BMC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from BMC import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',include('login.urls',namespace="login")),
    path('', include('home.urls',namespace="home")),
    path('monitor/', include('monitor.urls',namespace="monitor")),
    path('mail/', include('message.urls',namespace="message")),
    path('bmc_admin/', include('bmc_admin.urls',namespace="bmc_admin")),

] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

#+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT,)
