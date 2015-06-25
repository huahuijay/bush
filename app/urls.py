from django.conf.urls import include, url
from tastypie.api import Api
from app import views

urlpatterns = [
    #url(r'plateform.html$', views.plateform),
    #url(r'project.html$', views.project),
    #url(r'project_group.html$', views.project_group),
    url(r'^login$', views.login_view,name="login"),
    url(r'^logout$', views.logout_view),

    url(r'^suite$', views.suite_list, name="suite_list"),
    url(r'^suite/create$', views.suite_create, name="suite_create"),
    url(r'^suite/view/(?P<pk>\d+)$', views.suite_view, name="suite_view"),
    url(r'^suite/addsuite/(?P<pk>\d+)$', views.add_suite_view, name="add_suite_list"),
    url(r'^suite/add_suite/(?P<f_suite_pk>\d+)/(?P<suite_pk>\d+)$', views.add_suite, name="add_suite"),
    url(r'^suite/addcase/(?P<pk>\d+)$', views.add_case_view, name="add_case_list"),
    url(r'^suite/add_case/(?P<f_suite_pk>\d+)/(?P<case_pk>\d+)$', views.add_case, name="add_case"),
    url(r'^suite/edit/(?P<pk>\d+)$', views.suite_edit, name="suite_edit"),
    url(r'^suite/del/(?P<pk>\d+)$', views.suite_delete, name="suite_del"),
    url(r'^suite/del/(?P<pk>\d+)/(?P<suite_pk>\d+)$', views.suite_remove, name="remove_suite"),
    #url(r'suite/view/(?P<pk>\d+)$', views.suite_view, name="suite_view"),

    url(r'^case$', views.case_list, name="case_list"),
    url(r'^case/(?P<pk>\d+)$', views.case_list_index, name="case_list_index"),
    url(r'^case/create $', views.case_create, name="case_create"),
    url(r'^case/view/(?P<pk>\d+)$', views.case_view, name="case_view"),
    url(r'^case/edit/(?P<pk>\d+)$', views.case_edit, name="case_edit"),
    url(r'^case/del/(?P<pk>\d+)$', views.case_delete, name="case_delete"),
    url(r'^case/del/(?P<pk>\d+)/(?P<case_pk>\d+)$', views.case_remove, name="remove_case"),

    # url(r'^task$', views.task_list, name="task_list"),
    # url(r'^task/(?P<pk>\d+)$', views.task_list_index, name="task_list_index"),
    # url(r'^task/create/(?P<pk>\d+)$', views.task_create, name="task_create"),
    # url(r'^task/view/(?P<pk>\d+)$', views.task_view, name="task_view"),
    # url(r'^task/edit/(?P<pk>\d+)$', views.task_edit, name="task_edit"),
    # url(r'^task/del/(?P<pk>\d+)$', views.task_delete, name="task_delete"),
    url(r'^task/trigger/(?P<pk>\d+)$', views.task_trigger, name="task_trigger"),

    url(r'task_case/del/(?P<pk_task>\d+)/(?P<pk_case>\d+)$', views.task_case_delete, name="task_case_delete"),


    url(r'^machine$', views.machine_list, name="machine_list"),
    # url(r'^machine/(?P<pk>\d+)$', views.machine_list_index, name="machine_list_index"),
    url(r'^machine/create/(?P<pk>\d+)$', views.machine_create, name="machine_create"),
    url(r'^machine/view/(?P<pk>\d+)$', views.machine_view, name="machine_view"),
    url(r'^machine/edit/(?P<pk>\d+)$', views.machine_edit, name="machine_edit"),
    url(r'^machine/del/(?P<pk>\d+)$', views.machine_delete, name="machine_delete"),



    url(r'^script$', views.script_list, name="script_list"),
    url(r'^script/view$', views.script_view),
    #url(r'machine/edit/(?P<pk>\d+).html$', views.machine_edit, name="machine_edit"),
    #url(r'script/del/(?P<pk>\d+).html$', views.script_delete, name="script_delete"),

    url(r'^report$', views.report_list, name="report_list"),
    # url(r'^report/(?P<pk>\d+)$', views.report_list_index, name="report_list_index"),
    url(r'^report/task/(?P<pk>\d+)$', views.report_task_list, name="report_task_list"),


    url(r'demo_celery.html$', views.demo_celery, name="demo_celery"),


    #url(r'index', views.index),
    url(r'^$', views.suite_list),
    url(r'index.html$', views.suite_list),
]
