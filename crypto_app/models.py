from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

import random
import string
import json
from uuid import uuid4

from account.models import Account


def rand_str(size):
    code = str(uuid4()).replace('-', '')[:size]
    code_upper = code.upper()
    return code_upper


def rand_unique_str():
    letters = string.ascii_uppercase + string.digits
    size = 50
    return  ''.join(random.choice(letters) for _ in range(size))


class Transactions(models.Model):
    user =  models.ForeignKey(Account,related_name='user_transactions', on_delete=models.CASCADE,null=True, blank=True)
    trans_type = models.CharField(max_length=50)
    wallet_address = models.CharField(max_length=50,blank=True,null=True)
    amount_in_coin = models.FloatField( blank=True,null=True)
    amount_in_usd = models.IntegerField( blank=True,null=True)
    coin_tpye = models.CharField(max_length=50,blank=True,null=True)
    date = models.DateTimeField(blank=True,null=True)
    uri = models.CharField(max_length=50, default=rand_str(30))
    is_approved = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.user.username} :  {self.trans_type}"


class POP(models.Model):
    user =  models.ForeignKey(Account,related_name='user_pop', on_delete=models.CASCADE,null=True, blank=True)
    amount_in_coin = models.FloatField( blank=True,null=True)
    amount_in_usd = models.IntegerField( blank=True,null=True)
    coin_tpye = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    approved_dated = models.DateTimeField(blank=True,null=True)
    is_approved = models.BooleanField(default=False)
    uri = models.CharField(max_length=50, default=rand_str(30))
    status = models.CharField(max_length=40,default="approved")


    def __str__(self):
        return f"{self.user.username} :  {self.amount_in_usd}"


STATUS = (
    ("active","active"),
    ("inactive","inactive"),
    ("pending","pending"),
    ("completed","completed"),
)

class Investments(models.Model):

    user =  models.OneToOneField(Account, on_delete = models.CASCADE)
    amount_invested = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    end_date =  models.DateTimeField(blank=True,null=True)
    start_date =  models.DateTimeField(blank=True,null=True)
    crediting_date =  models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=40, choices=STATUS,default="inactive")
    amount_earn = models.IntegerField(default=0)
    pop =  models.ForeignKey(POP,related_name='investment_pop', on_delete=models.CASCADE,null=True, blank=True)
    uri = models.CharField(max_length=50, default=rand_str(30))

    def __str__(self):
        return f"{self.user.username} :  {self.amount_invested}"




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_investmet(sender,instance=None, created=False, **kwargs):
    if created:
        Investments.objects.create(user=instance,amount_invested=0)
