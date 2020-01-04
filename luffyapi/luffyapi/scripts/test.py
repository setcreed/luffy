import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "luffyapi.settings.dev")
django.setup()

from home import views
print(views)

# from utils.logging import logger
# logger.critical('asf')
