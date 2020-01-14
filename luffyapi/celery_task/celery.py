# 一、加载django配置环境
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "luffyapi.settings.dev")

# 二、加载celery配置环境
from celery import Celery
# broker
broker = 'redis://127.0.0.1:6379/14'
# backend
backend = 'redis://127.0.0.1:6379/15'
# worker
app = Celery(broker=broker, backend=backend, include=['celery_task.tasks'])


# 时区
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False

# 定时任务配置
from datetime import timedelta
from celery.schedules import crontab
app.conf.beat_schedule = {
    # 'add-task': {
    #     'task': 'celery_task.tasks.add',
    #     'schedule': timedelta(seconds=3),
    #     # 'schedule': crontab(hour=8, day_of_week=1),  # 每周一早八点
    #     'args': (20, 10),
    # },
    # 'low-task': {
    #     'task': 'celery_task.tasks.low',
    #     'schedule': timedelta(seconds=6),
    #     'args': (20, 10),
    # },
    # 'get-users-task': {
    #     'task': 'celery_task.tasks.get_users',
    #     'schedule': timedelta(seconds=3),
    #     'args': (),
    # },
    # 案例：django异步更新缓存
    'update-banner-cache': {
        'task': 'celery_task.tasks.update_banner_cache',
        'schedule': timedelta(seconds=10),
        'args': (),
    },
}

"""
celery框架工作流程
1）创建Celery框架对象app，配置broker和backend，得到的app就是worker
2）给worker对应的app添加可处理的任务函数，用include配置给worker的app
3）完成提供的任务的定时配置app.conf.beat_schedule
4）启动celery服务，运行worker，执行任务
5）启动beat服务，运行beat，添加任务
"""