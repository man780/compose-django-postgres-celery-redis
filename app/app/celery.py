import os
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# from core.models import Account

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls every 10 minutes.
    sender.add_periodic_task(10.0, clear_holds, name='every 10')


logger = get_task_logger(__name__)

@app.task
def clear_holds():
    from core.models import Account
    accounts = Account.objects.all()
    isAllCleared = True
    for account in accounts:
        if account.hold == 0:
            continue
        result = account.balance - account.hold
        if result>=0:
            account.balance = result
            account.hold = 0
            account.save()
            logger.info("Account hold cleared. - " + account.fio)
        else:
            isAllCleared = False
            logger.warning("Account hold not cleared - " + account.fio)
    if isAllCleared:
        logger.info("+++All account holds cleared.+++")
    else:
        logger.info("---Not all account holds cleared.---")
    return 1

app.autodiscover_tasks()
