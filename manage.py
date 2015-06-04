#!/usr/bin/env python
import os
import sys
import requests
import threading
import time


class QueryAndFillSQL(threading.Thread):
    Running = False
    url = '/'.join(['http://127.0.0.1:8000/api/v1', 'get_result'])
    def run(self):
        QueryAndFillSQL.Running = True
        while True:
            print 123
            time.sleep(5)
            requests.get(QueryAndFillSQL.url)

if not QueryAndFillSQL.Running:
    print 'asfashasklfhalskfhalkfalsjkf'
    p_deamon = QueryAndFillSQL()
    p_deamon.daemon = True
    p_deamon.start()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "staf.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
