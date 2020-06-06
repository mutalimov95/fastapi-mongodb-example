from celery import Celery

celery_app = Celery("worker", broker="amqp://guest@0.0.0.0:5672//")

celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
