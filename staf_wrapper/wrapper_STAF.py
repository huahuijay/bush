#!/usr/bin/python
# -*-coding:utf-8-*-


import time

from PySTAF import *
from PySTAFMon import *
from PySTAFLog import *


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
        self.job_id = None

    def register(self):
        try:
            self.handle = STAFHandle("demo_livecd")
        except STAFException, e:
            print "Error registering with STAF, RC: %d" % e.rc

    def execute(self):
        self.result = self.handle.submit('local', 'stax',
                                         'execute file {STAF/Env/HOME}/PycharmProjects/STAF/staf/staf_wrapper/litian_case.xml')
        if self.result.rc != STAFResult.Ok:
            raise Exception, 'Error on execute stax task, RC: %d, Result: %s' % (result.rc, result.result)
        self.job_id = self.result.result
        return self.result.result

    def query(self):
        self.result = self.handle.submit('local', 'stax',
                                         'get result job {0} details'.format(self.job_id)).resultContext.getRootObject()
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


if __name__ == '__main__':
    test()