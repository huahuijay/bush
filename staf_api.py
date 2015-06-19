#! /usr/bin/env python
import requests
import time

url_prefix = 'http://172.29.10.101:8000/api/v1'


def query_suite():
    url = '/'.join([url_prefix, 'query_suite'])
    print url
    return requests.get(url).json()


def query_task(suite_id):
    url = '/'.join([url_prefix, 'query_task', '{}'.format(suite_id)])
    print url
    return requests.get(url).json()


def trigger_deb(task_id):
    url = '/'.join([url_prefix, 'trigger_deb', 'non-blocking', '{}'.format(task_id)])
    print url
    return requests.get(url).json()


def get_result(job_id, machine_ip):
    url = '/'.join([url_prefix, 'get_result', '{}'.format(job_id), '{}'.format(machine_ip)])
    print url
    return requests.get(url).json()


if __name__ == '__main__':
    print query_suite()
    print query_task('2')
    print trigger_deb('8')
    print get_result('1', '172.29.10.195')