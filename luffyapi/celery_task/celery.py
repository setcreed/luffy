# 一、加载django配置环境
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "luffyapi.settings.dev")

from celery import Celery
broker = 'redis://127.0.0.1:6379/14'
backend = 'redis://127.0.0.1:6379/15'

app = Celery(broker=broker, backend=backend, include=['celery_task.tasks'])

# 时区
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False

# 任务的定时配置
from datetime import timedelta
from celery.schedules import crontab
app.conf.beat_schedule = {
    'update-banner-cache': {
        'task': 'celery_task.tasks.update_banner_cache',
        'schedule': timedelta(seconds=10),
        'args': (),
    }
}
