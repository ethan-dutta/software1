# from celery import Celery
# import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
# app = Celery('myproject')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# # RabbitMQ configuration
# app.conf.update(
#     broker_url='pyamqp://guest@localhost//',
#     result_backend='rpc://',
#     task_serializer='json',
#     accept_content=['json'],
#     result_serializer='json',
#     timezone='UTC',
#     enable_utc=True,
# )
# app.autodiscover_tasks()
