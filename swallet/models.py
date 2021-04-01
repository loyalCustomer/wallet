from django.db import models
from django.contrib.auth.models import User



class SimpleWallet(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_name = models.CharField('произвольное имя',max_length=250)
    ballance_rub = models.DecimalField(max_digits=20,decimal_places=2,default=0)

    def __str__(self):
        #return self.username.username
        return self.wallet_name

class Transaction(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_id = models.ForeignKey(SimpleWallet, on_delete=models.CASCADE)
    amount_rub = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250, blank=True, null=True)