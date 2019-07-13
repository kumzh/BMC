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
app_name ='[MessageConfig]'
urlpatterns = [
    path('', views.mesg,name="mesg"),
    path('target_set/', views.target_set,name="target_set"),
    path('to_mail_add/',views.to_mail_add,name="to_mail_add"),
    path('to_mail_test/',views.to_mail_test,name="to_mail_test"),
    path('mail_test/', views.mail_test,name="mail_test"),
    path("from_delete-<str:nid>/", views.from_delete, name='from_delete'),
    path("to_mail_add/to_delete-<str:nid>/", views.to_delete, name='to_delete'),
    path("target_set/target_delete-<str:nid>/", views.target_delete, name='target_delete'),


]
