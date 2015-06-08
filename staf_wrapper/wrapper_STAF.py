#!/usr/bin/python
# -*-coding:utf-8-*-
from PySTAF import *
# from PySTAFMon import *
# from PySTAFLog import *
import time


# following is a sample of format of test result
# '''
# {
# 'status': 'Normal',
# 'staf-map-class-name': 'STAF/Service/STAX/GetDetailedResult',
# 'scriptList': [],
# 'jobLogErrors': [],
# 'xmlFileName': '/home/chale/PycharmProjects/first_demo/demo.xml',
# 'function': 'func_test',
# 'startTimestamp': '20150521-10:17:36',
# 'testcaseList':
# [
# 	{'staf-map-class-name': 'STAF/Service/STAX/QueryTestcase',
# 	'information': '',
# 	'startedTimestamp': '20150521-10:17:36',
# 	'lastStatus': 'pass',
# 	'lastStatusTimestamp': '20150521-10:17:52',
# 	'elapsedTime': '00:00:16',
# 	'testcaseName': 'TestA',
# 	'numStarts': '4',
# 	'testcaseStack': ['TestA'],
# 	'numPasses': '1',
# 	'numFails': '3'
# 	},
# 	{'staf-map-class-name': 'STAF/Service/STAX/QueryTestcase',
# 	'information': '',
# 	'startedTimestamp': '20150521-10:17:52',
# 	'lastStatus': 'fail',
# 	'lastStatusTimestamp': '20150521-10:18:09',
# 	'elapsedTime': '00:00:17',
# 	'testcaseName': 'TestB',
# 	'numStarts': '4',
# 	'testcaseStack': ['TestB'],
# 	'numPasses': '1',
# 	'numFails': '3'}
# ],
# 'scriptFileList': [],
# 'fileMachine': 'local://local',
# 'jobName': None,
# 'result': 'None',
# 'testcaseTotals':
# {
# 	'staf-map-class-name': 'STAF/Service/STAX/TestcaseTotals',
# 	'numFails': '6',
# 	'numPasses': '2',
# 	'numTests': '2'
# },
# 'scriptMachine': None,
# 'endTimestamp': '20150521-10:18:09',
# 'arguments': None}
# '''

class STAFWrapper(object):
    def __init__(self):
        self.handle = None
        self.result = None
        self.detect_ret_value = None
        self._register()
        self.handle.submit('local', 'event', 'register type monitor subtype properties')
        self.handle.submit('local', 'event', 'register type monitor subtype endoftest')

    def _register(self):
        try:
            self.handle = STAFHandle("demo_livecd")
        except STAFException, e:
            print "Error registering with STAF, RC: %d" % e.rc

    def detect_device(self, device_IP):
        result = self.handle.submit(device_IP, 'ping', 'ping')
        if result.result == 'PONG':
            self.detect_ret_value = 1
        else:
            self.detect_ret_value = 2

    def execute(self, xml_name):
        xml_location = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media', 'case', xml_name)
        result = self.handle.submit('local', 'stax',
                                         'execute file {0}.xml'.format(xml_location))
        if result.rc != STAFResult.Ok:
            raise Exception, 'Error on execute stax task, RC: %d, Result: %s' % (result.rc, result.result)
        return result.result

    def query(self, job_id):
        self.result = self.handle.submit('local', 'stax',
                                         'get result job {0} details'.format(job_id)).resultContext.getRootObject()
        if type(self.result) is dict:
            return 0
        else:
            return 1

    def unregister(self):
        try:
            self.handle.unregister()
            return 0
        except STAFException, e:
            print "Error unregistering static handle with STAF, RC: %d" % e.rc
            return 1


def test():
    staf_obj = STAFWrapper()
    staf_obj._register()
    staf_obj.execute('task_name')
    while True:
        result = staf_obj.handle.submit('local', 'queue', 'get wait')
        property_dict = result.resultContext.getRootObject()
        try:
            status = property_dict['message']['propertyMap']['status']
            print 'status', status
            case_name = property_dict['message']['propertyMap']['case_name']
            print 'case_name', case_name
        except KeyError, e:
            pass
        if property_dict['message']['subtype'] == 'endoftest':
            time.sleep(3)
            break





if __name__ == '__main__':
    test()