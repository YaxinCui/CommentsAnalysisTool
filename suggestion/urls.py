from django.conf.urls import url
from . import views # 从当前目录导入views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^result/', views.result, name='result'),
]