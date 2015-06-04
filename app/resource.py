from django.conf.urls import url
from tastypie.resources import Resource
from tastypie.utils import trailing_slash

from staf_wrapper import wrapper_STAF
import utils
import time
import os
from models import *


class ProjectStafResource(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.staf_obj = wrapper_STAF.STAFWrapper()
        self.staf_obj.register()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/?$" % self._meta.resource_name, self.wrap_view('staf_api'), name='staf_api'),
            # following is new APIs
            url(r"^trigger_deb/(?P<mode>.+)/(?P<task_name>.+?/?)$", self.wrap_view('trigger_deb'), name='trigger_deb'),
            url(r"^trigger_iso/(?P<mode>.+)/(?P<task_name>.+?/?)$", self.wrap_view('trigger_iso'), name='trigger_iso'),
            url(r"^get_result/(?P<staf_handle_key>.+/?)?$", self.wrap_view('get_result'), name='get_result'),
            url(r"^query_task/(?P<suite_name>.+?)/?$", self.wrap_view('query_task'), name='query_task'),
            url(r"^query_suite/?$", self.wrap_view('query_suite'), name='query_suite'),
        ]

    def query_suite(self, request, **kwargs):
        suite_list = list()
        suites = Suite.objects.all()
        for suite in suites:
            suite_struct_dict = dict()
            suite_struct_dict['id'] = suite.id
            suite_struct_dict['name'] = suite.name
            suite_list.append(suite_struct_dict)
            # data_struct.setdefault(suite.name, dict())
            # tasks = suite.task_set.all()
            # for task in tasks:
            #     data_struct[suite.name].setdefault(task.name, list())
            #     task_cases = task.task_case_set.all()
            #     for taskcase in task_cases:
            #         data_struct[suite.name][task.name].append(taskcase.case.__dict__)
        return self.create_response(request, {"key": suite_list})

    def query_task(self, request, **kwargs):
        task_list = list()
        suite_name = kwargs['suite_name']
        tasks = Suite.objects.get(name=suite_name).task_set.all()

        for task in tasks:
            task_struct_dict = dict()
            task_struct_dict['name'] = task.name
            task_struct_dict['id'] = task.id
            task_list.append(task_struct_dict)
            # data_struct.setdefault(task.name, list())
            # task_cases = task.task_case_set.all()
            # for taskcase in task_cases:
            #     data_struct[task.name].append(taskcase.case.__dict__)
        return self.create_response(request, {"key": task_list})


    def trigger_deb(self, request, **kwargs):
        if kwargs['mode'] == u'non-blocking':
            exec_handle = self.staf_obj.execute(kwargs['task_name'])
            return self.create_response(request, {"key": exec_handle})
        else:
            raise

    def trigger_iso(self, request, **kwargs):
        pass

    def get_result(self, request, **kwargs):
        parameter = kwargs['staf_handle_key']
        if parameter is None:
            staf_handle_key = utils.tmp_handle_global
        else:
            staf_handle_key = kwargs['staf_handle_key']
        if self._query(staf_handle_key) == 'on-going':
            return self.create_response(request, {"key": 'on-going'})
        else:
            test_attributes = self.staf_obj.result['testcaseList']
            xml_file = self.staf_obj.result['xmlFileName']
            task_name = os.path.splitext(os.path.basename(xml_file))[0]
            for test_attribute in test_attributes:
                if test_attribute['lastStatus'] == 'pass':
                    test_result = 1
                else:
                    test_result = 2
                case_name = test_attribute['testcaseStack'][0]
                # Case.objects.get(name=case_name)
                try:
                    report = Report.objects.get(case=Case.objects.get(name=case_name))
                except Exception,e:
                    Report(case=Case.objects.get(name=case_name), task=Task.objects.get(name=task_name), result=test_result).save()
                else:
                    report.result = test_result
                    report.save()

            return self.create_response(request, {"key": self.staf_obj.result})

    def _query(self, exec_handle):
        if self.staf_obj.query(job_id=exec_handle) == 0:
            return 'has-done'
        else:
            return 'on-going'

    def _unregister(self):
        if self.staf_obj.unregister() == 0:
            return 'successful'
        else:
            return 'unsuccessful'

    def staf_api(self, request, **kwargs):
        staf_obj = wrapper_STAF.STAFWrapper()
        staf_obj.register()
        staf_obj.execute()
        while True:
            time.sleep(5)
            # successful
            if staf_obj.query() == 0:
                print staf_obj.result
                break
            # unsuccessful
            else:
                print 'is on-going'
        staf_obj.unregister()

        return self.create_response(request, {"key": staf_obj.result})

    class Meta:
        resource_name = 'staf'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
