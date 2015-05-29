#! /usr/bin/env python
import requests
import time

url_prefix = 'http://172.3.3.101:8000/api/v1'

#
# def initialize():
#     return requests.get('http://172.29.10.101:8000/api/v1/initialize').json()
#
#
# def trigger_litian(deb_location):
#     print 'http://172.29.10.101:8000/api/v1/non_blocking_trigger_litian/{0}'.format(deb_location)
#     return requests.get('http://172.29.10.101:8000/api/v1/non_blocking_trigger_litian/{0}'.format(deb_location)).json()
#
#
# def query(num):
#     print 'http://172.29.10.101:8000/api/v1/query/{0}'.format(num)
#     return requests.get('http://172.29.10.101:8000/api/v1/query/{0}/'.format(num)).json()
#
# def unregister(num):
#     return requests.get('http://172.29.10.101:8000/api/v1/unregister/{0}'.format(num)).json()

def trigger_deb(test_suite_name, mode='non-blocking'):
    url = '/'.join([url_prefix, r'trigger_deb', mode, test_suite_name])
    print url
    return requests.get(url).json()

def get_result(job_ID):
    url = '/'.join([url_prefix, r'get_result', job_ID])
    print url
    return requests.get(url).json()


if __name__ == '__main__':
    job_ID = trigger_deb('testsuite')['key']
    get_result(job_ID)
    # print initialize()
    # staf_id = trigger_litian('172.29.50.21/cbsfiles/pool/main/g/gedit/gedit-common_3.10.4-0ubuntu4_all.deb')['key']
    # while True:
    #     time.sleep(1)
    #     if query(staf_id)['key'] != 'on-going':
    #         break
    # print query(staf_id)['key']
    # print unregister(staf_id)