
from django.contrib import admin
from .models import SimpleWallet, Transaction
from django.contrib.auth.models import User


admin.site.register(SimpleWallet)
admin.site.register(Transaction)