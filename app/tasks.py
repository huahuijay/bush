import time
import os
import threading
import Queue

from celery import task

from models import *
from staf_wrapper.wrapper_STAF import staf_obj


@task()
def loop_machine_status():
    machines = Machine.objects.all()
    for machine in machines:
        machine.status = staf_obj.detect_device(machine.address)
        machine.save()

@task()
def monitor(staf_obj, exec_handle):
    while True:
        result = staf_obj.handle.submit('local', 'queue', 'get wait')
        property_dict = result.resultContext.getRootObject()
        try:
            status = property_dict['message']['propertyMap']['status']
            if status == 'running':
                status = 3
            elif status == 'finish':
                status = 4
            else:
                raise 'Oops!!'
            print 'status', status
            case_name = property_dict['message']['propertyMap']['case_name']
            print 'case_name', case_name
            task_name = property_dict['message']['propertyMap']['task_name']
            print 'task_name', task_name

# save date into DB
            try:
                report = Report.objects.get(case=Case.objects.get(name=case_name))
            except Exception,e:
                Report(case=Case.objects.get(name=case_name), task=Task.objects.get(name=task_name), result=status).save()
            else:
                report.result = status
                report.save()
        except KeyError, e:
            pass
        if property_dict['message']['subtype'] == 'endoftest':
            time.sleep(3)
            if staf_obj.query(job_id=exec_handle) == 0:
                test_attributes = staf_obj.result['testcaseList']
                xml_file = staf_obj.result['xmlFileName']
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
                        try:
                            Report(case=Case.objects.get(name=case_name), task=Task.objects.get(name=task_name), result=test_result).save()
                        except Exception:
                            pass
                    else:
                        report.result = test_result
                        report.save()
            else:
                raise 'it must be a mistake!'
            break