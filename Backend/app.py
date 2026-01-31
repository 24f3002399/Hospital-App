from flask import Flask 
from application.config import LocalDevelopmentConfig
from application.extentions import db
from application.models import Users
from application.security import jwt
from flask_cors import CORS
from application.celery_init import celery_init_app
from celery.schedules import crontab

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    app.app_context().push()
    return app

app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()

@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=7, day_of_month='1'),     # (minute = '*/2') -> after every 2 minute
        monthly_report.s(),
    )

    sender.add_periodic_task(
        crontab(minute=0, hour=7), 
        daily_update.s()
    )

from application.routes import *

if __name__ == "__main__":
    app.run()