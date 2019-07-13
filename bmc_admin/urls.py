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

from django.urls import path
from . import views
app_name ='[BmcAdminConfig]'
urlpatterns = [
    path('', views.bmc_admin,name="bmc_admin"),  #加了name后，在HTML中可以用{%url 'bmc_admin'%}的方式访问
    path('snmp_test/', views.snmp_test,name="snmp_test"),
    path("delete-<str:nid>/", views.delete, name='delete'),

]
