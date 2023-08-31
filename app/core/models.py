import uuid
from django.db import models
from django.urls import reverse


class Account(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    fio = models.CharField(max_length=100)
    balance = models.IntegerField(default=0)
    hold = models.IntegerField(default=0)
    status = models.BooleanField()

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Account'

    def get_absolute_url(self):
        return reverse('account', args=[str(self.uuid)])

    def increase_balance(self, value):
        self.balance = self.balance + value
        self.save()
        return True

    def decrease_balance(self, value):
        result = self.balance - self.hold - value
        if result<0:
            return False
        self.balance = result
        self.hold = 0
        self.save()
        return True
