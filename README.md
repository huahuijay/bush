# 简介

自动化测试WEB服务

servser需要配置

    1.手动安装STAF，方法请参考http://10.3.3.42/wiki/index.php/STAF%26STAX%E5%AE%89%E8%A3%85%E6%89%8B%E5%86%8C
    2.export PYTHONPATH=/usr/local/staf/lib:$PYTHONPATH
    3.cd /usr/local/staf/lib
    cp python27/PYSTAF.so .

#######################分割######################################

目前我们使用django-celery 来进行定时控制和异步队列操作。

所以需要在开启django之后，需要进行如下操作：
1.将setting文件中的如下代码取消注释
# CELERYBEAT_SCHEDULE = {
#    'add-every-120-seconds': {
#        'task': 'app.tasks.loop_machine_status',
#        'schedule': timedelta(seconds=120),
#    },
# }
2.在项目路径下输入如下命令：
python manage.py celery worker --loglevel=info &
python manage.py celery beat &

3.我们可以通过该url查看task是否已经完成：http://127.0.0.1:8000/admin/djcelery/intervalschedule/

4.在确认成功创建这个任务之后，请注释掉1中的代码。（否则，会重复创建该任务）

#######################分割######################################

rest api使用说明：
1.http://127.0.0.1:8000/api/v1/query_suite
{"key": [{"id": 1, "name": "suite_name"}, {"id": 2, "name": "suite_name2"}]}
2.http://127.0.0.1:8000/api/v1/query_task/2
{"key": [{"id": 2, "name": "task_name2", "suite": "suite_name2"}, {"id": 3, "name": "task_name_new1_under_suite2", "suite": "suite_name2"}, {"id": 4, "name": "task_name_new2_under_suite2", "suite": "suite_name2"}, {"id": 5, "name": "task_name_new3_under_suite2", "suite": "suite_name2"}, {"id": 6, "name": "fasdf", "suite": "suite_name2"}, {"id": 7, "name": "task_name_new5_under_suite2", "suite": "suite_name2"}, {"id": 8, "name": "task_name_new_new_under_suite2", "suite": "suite_name2"}]}
3.http://127.0.0.1:8000/api/v1/trigger_deb/non-blocking/8
{"handle": "14", "task_name": "task_name_new_new_under_suite2", "machine_ip: "172.29.10.195""}
4.http://127.0.0.1:8000/api/v1/get_result/14/172.29.10.195
{"key": "on-going"} 或者
{"arguments": null, "endTimestamp": "20150617-15:30:54", "fileMachine": "tcp://10.3.30.207@6500", "function": "func_test", "jobLogErrors": "[]", "jobName": null, "result": "None", "scriptFileList": [], "scriptList": [], "scriptMachine": null, "staf-map-class-name": "STAF/Service/STAX/GetDetailedResult", "startTimestamp": "20150617-15:30:39", "status": "Normal", "testcaseList": [{"elapsedTime": "00:00:05", "information": "", "lastStatus": "fail", "lastStatusTimestamp": "20150617-15:30:44", "numFails": "1", "numPasses": "0", "numStarts": "1", "staf-map-class-name": "STAF/Service/STAX/QueryTestcase", "startedTimestamp": "20150617-15:30:40", "testcaseName": "case_name11", "testcaseStack": ["case_name11"]}, {"elapsedTime": "00:00:04", "information": "", "lastStatus": "pass", "lastStatusTimestamp": "20150617-15:30:49", "numFails": "0", "numPasses": "1", "numStarts": "1", "staf-map-class-name": "STAF/Service/STAX/QueryTestcase", "startedTimestamp": "20150617-15:30:45", "testcaseName": "case_name12", "testcaseStack": ["case_name12"]}, {"elapsedTime": "00:00:04", "information": "", "lastStatus": "pass", "lastStatusTimestamp": "20150617-15:30:53", "numFails": "0", "numPasses": "1", "numStarts": "1", "staf-map-class-name": "STAF/Service/STAX/QueryTestcase", "startedTimestamp": "20150617-15:30:49", "testcaseName": "case_name13", "testcaseStack": ["case_name13"]}, {"elapsedTime": "00:00:02", "information": "", "lastStatus": "pass", "lastStatusTimestamp": "20150617-15:30:54", "numFails": "0", "numPasses": "2", "numStarts": "2", "staf-map-class-name": "STAF/Service/STAX/QueryTestcase", "startedTimestamp": "20150617-15:30:39", "testcaseName": "last_case", "testcaseStack": ["last_case"]}], "testcaseTotals": {"numFails": "1", "numPasses": "4", "numTests": "4", "staf-map-class-name": "STAF/Service/STAX/TestcaseTotals"}, "xmlFileName": "/home/chale/work/staf/media/case/task_name_new_new_under_suite2.xml"}