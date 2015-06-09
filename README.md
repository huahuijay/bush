# 简介

自动化测试WEB服务

servser需要配置

    1.手动安装STAF，方法请参考http://10.3.3.42/wiki/index.php/STAF%26STAX%E5%AE%89%E8%A3%85%E6%89%8B%E5%86%8C
    2.export PYTHONPATH=/usr/local/staf/lib:$PYTHONPATH
    3.cd /usr/local/staf/lib
    cp python27/PYSTAF.so .



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
