from django.conf.urls import include, url
from tastypie.api import Api
from app import views

urlpatterns = [
    url(r'plateform', views.plateform),
    url(r'project', views.project),
    url(r'project_group', views.project_group),
    url(r'case', views.case),
    url(r'^$', views.index),

]
