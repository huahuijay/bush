from django.conf.urls import include, url
from tastypie.api import Api
from app import views

urlpatterns = [
    url(r'plateform.html$', views.plateform),
    url(r'project.html$', views.project),
    url(r'project_group.html$', views.project_group),
    url(r'suite.html$', views.suite_list),
    url(r'case.html$', views.case_list),
    url(r'script.html$', views.script_list),
    url(r'script_show.html$', views.script_show),
    url(r'case/del/(?P<pk>\d+).html$', views.case_delete, name="case_delete"),
    #url(r'index', views.index),
    url(r'^$', views.case_list),
    url(r'index.html$', views.case_list),
]
