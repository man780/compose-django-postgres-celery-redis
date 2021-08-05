from celery import shared_task
from .models import Account


@shared_task
def count_accounts():
    return Account.objects.count()


@shared_task
def clear_hold():
    accounts = Account.objects.all()
    for account in accounts:
        result = account.balance - account.hold
        if result>=0:
            account.balance = result
            account.hold = 0
            account.save()

    return True
