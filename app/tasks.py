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
def monitor(staf_obj, exec_handle, p_task_report, machine_ip):
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
                case_report = Case_Report.objects.get(task_report=p_task_report, case=Case.objects.get(name=case_name))
            except Exception:
                Case_Report(task_report=p_task_report, case=Case.objects.get(name=case_name), result=status).save()
            else:
                case_report.result = status
                case_report.save()
        except KeyError, e:
            pass

        if property_dict['message']['subtype'] == 'endoftest':
            p_task_report.result = 4
            p_task_report.save()
            time.sleep(3)
            if staf_obj.query(job_id=exec_handle, location=machine_ip) == 0:
                if staf_obj.result['testcaseTotals']['numFails'] == '0':
                    p_task_report.result = 1 # pass
                    p_task_report.save()
                else:
                    p_task_report.result = 2 # fail
                    p_task_report.save()
                test_attributes = staf_obj.result['testcaseList']
                xml_file = staf_obj.result['xmlFileName']
                for test_attribute in test_attributes:
                    if test_attribute['lastStatus'] == 'pass':
                        test_result = 1
                    else:
                        test_result = 2
                    case_name = test_attribute['testcaseStack'][0]
                    # Case.objects.get(name=case_name)
                    try:
                        try:
                            case_report = Case_Report.objects.get(task_report=p_task_report, case=Case.objects.get(name=case_name))
                        except Exception:
                            Case_Report(task_report=p_task_report, case=Case.objects.get(name=case_name), result=test_result).save()
                        else:
                            case_report.result = test_result
                            case_report.save()
                    except Exception:
                        pass # for the latest case specially
            else:
                raise 'it must be a mistake!'
            break