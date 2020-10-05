from django.db import models

from accounts.models import Account
from orders.models import Order


class ShippingAddr(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=128, null=False)
    city = models.CharField(max_length=128, null=False)
    state = models.CharField(max_length=128, null=False)
    zipcode = models.CharField(max_length=128, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
