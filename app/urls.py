from django.conf.urls import include, url
from tastypie.api import Api
from app import views

urlpatterns = [
    #url(r'plateform.html$', views.plateform),
    #url(r'project.html$', views.project),
    #url(r'project_group.html$', views.project_group),
    url(r'suite.html$', views.suite_list),
    url(r'suite/view/(?P<pk>\d+).html$', views.suite_view, name="suite_view"),
    url(r'case.html$', views.case_list, name="case_list"),
    url(r'case/view/(?P<pk>\d+).html$', views.case_view, name="case_view"),
    url(r'case/del/(?P<pk>\d+).html$', views.case_delete, name="case_delete"),
    url(r'task.html$', views.task_list),
    url(r'task/view/(?P<pk>\d+).html$', views.task_view, name="task_view"),
    url(r'script_add.html$', views.script_add),
    url(r'script_view.html$', views.script_view),

    #url(r'index', views.index),
    url(r'^$', views.case_list),
    url(r'index.html$', views.case_list),
]
