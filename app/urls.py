from django.conf.urls import include, url
from tastypie.api import Api
from app import views

urlpatterns = [
    #url(r'plateform.html$', views.plateform),
    #url(r'project.html$', views.project),
    #url(r'project_group.html$', views.project_group),
    url(r'login.html$', views.login_view),
    url(r'logout.html$', views.logout_view),

    url(r'suite.html$', views.suite_list, name="suite_list"),
    url(r'suite/view/(?P<pk>\d+).html$', views.suite_view, name="suite_view"),

    url(r'case.html$', views.case_list, name="case_list"),
    url(r'case/view/(?P<pk>\d+).html$', views.case_view, name="case_view"),
    url(r'case/edit/(?P<pk>\d+).html$', views.case_edit, name="case_edit"),
    url(r'case/del/(?P<pk>\d+).html$', views.case_delete, name="case_delete"),

    url(r'task.html$', views.task_list, name="task_list"),
    url(r'task/view/(?P<pk>\d+).html$', views.task_view, name="task_view"),
    url(r'task/edit/(?P<pk>\d+).html$', views.task_edit, name="task_edit"),
    url(r'task/del/(?P<pk_task>\d+)/(?P<pk_case>\d+).html$', views.task_delete, name="task_delete"),
    url(r'task/trigger/(?P<pk>\d+).html$', views.task_trigger, name="task_trigger"),

    url(r'machine.html$', views.machine_list, name="machine_list"),
    url(r'machine/view/(?P<pk>\d+).html$', views.machine_view, name="machine_view"),
    url(r'machine/edit/(?P<pk>\d+).html$', views.machine_edit, name="machine_edit"),
    url(r'machine/del/(?P<pk>\d+).html$', views.machine_delete, name="machine_delete"),

    url(r'script_add.html$', views.script_add),
    url(r'script_view.html$', views.script_view),

    url(r'report.html$', views.report_list, name="report_list"),
    url(r'report/view/(?P<task_name>.+).html$', views.report_view, name="report_view"),
    # url(r'machine/edit/(?P<pk>\d+).html$', views.machine_edit, name="machine_edit"),
    # url(r'machine/del/(?P<pk>\d+).html$', views.machine_delete, name="machine_delete"),

    #url(r'index', views.index),
    url(r'^$', views.case_list),
    url(r'index.html$', views.case_list),
]
