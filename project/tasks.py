from .celery import app
from celery.schedules import crontab
from celery import shared_task

from disembursements.models import DisembursementController

# Periodic function that will create new disembursements on Mondays. The crontab settins are in the settings.py file.
@shared_task
def create_all_disembursements():
    DisembursementController.disembursements_generator()