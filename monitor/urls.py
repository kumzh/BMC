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

from django.urls import path,re_path
from monitor import views
app_name ='[MonitorConfig]'
urlpatterns = [
    re_path('^(?P<host_id>\d+)/total_mem$', views.total_mem, name='total_mem'),
    re_path('^(?P<host_id>\d+)/memo$', views.memo, name='memo'),
    re_path('^(?P<host_id>\d+)/cpu$', views.cpu, name='cpu'),
    re_path('^(?P<host_id>\d+)/cpu_ajax$', views.cpu_ajax, name='cpu_ajax'),
    re_path('^(?P<host_id>\d+)/summary$', views.home,name='home'),
    re_path('^(?P<host_id>\d+)/total$', views.total,name='total'),
    re_path('^(?P<host_id>\d+)/load$', views.load,name='load'),
    re_path('^(?P<host_id>\d+)/load_ajax$', views.load_ajax,name='load_ajax'),
    # re_path('^(?P<host_id>\d+)/run_time_ajax$', views.run_time_ajax,name='run_time_ajax'),
    # path("<int:nid>\d+/",views.home)    列表下钻

]
