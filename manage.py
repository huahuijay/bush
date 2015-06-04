#!/usr/bin/env python
import os
import sys


def start_daemon():
    import threading
    import time
    import app.utils
    from staf_wrapper.wrapper_STAF import STAFWrapper
    from app.models import Report, Case, Task


    class QueryAndFillSQL(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.staf_obj = STAFWrapper()
            self.staf_obj.register()

        def run(self):
            QueryAndFillSQL.Running = True
            while True:
                time.sleep(60)
                print 123
                if self.staf_obj.query(job_id=app.utils.tmp_handle_global) == 0:
                    app.utils.tmp_handle_global = None
                    print 456
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

                # requests.get(QueryAndFillSQL.url)

    print 'asfashasklfhalskfhalkfalsjkf'
    p_deamon = QueryAndFillSQL()
    p_deamon.daemon = True
    p_deamon.start()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "staf.settings")

    from django.core.management import execute_from_command_line

    start_daemon()
    execute_from_command_line(sys.argv)


