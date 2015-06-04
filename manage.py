#!/usr/bin/env python
import os
import sys
import requests
import threading
import time
import app.utils
from staf_wrapper.wrapper_STAF import STAFWrapper
from app.models import *


class QueryAndFillSQL(threading.Thread):
    Running = False
    url = '/'.join(['http://127.0.0.1:8000/api/v1', 'get_result'])
    def __init__(self):
        threading.Thread.__init__(self)
        self.staf_obj = STAFWrapper()
        self.staf_obj.register()

    def run(self):
        QueryAndFillSQL.Running = True
        while True:
            print 123

            if self.staf_obj.query(job_id=app.utils.tmp_handle_global) == 0:
                app.utils.tmp_handle_global = None
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
            time.sleep(60)
            # requests.get(QueryAndFillSQL.url)

if not QueryAndFillSQL.Running:
    print 'asfashasklfhalskfhalkfalsjkf'
    p_deamon = QueryAndFillSQL()
    p_deamon.daemon = True
    p_deamon.start()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "staf.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
