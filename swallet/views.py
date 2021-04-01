
'''
API сервиса должен позволять:
1. создавать, редактировать и удалять кошелек. +
2. создавать и удалять транзакции в рамках кошелька (при этом напрямую редактировать баланс кошелька пользователь не может)
транзакции могут быть как +, так и -. то есть транзакции по зачислению денег и списанию.
у каждой транзакции должна быть дата, сумма, произвольный комментарий от пользователя.
3. Просматривать список своих кошельков +
4. Просматривать список своих транзакций как в рамках одного кошелька, так и общий, всех кошельков сразу.+
'''
from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_204_NO_CONTENT

from .models import SimpleWallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer


@api_view(['GET','POST','PUT','PATCH','DELETE']) 
def get_wallets(request, user_id):
    if request.method == 'GET': #3. Просматривать список своих кошельков
        requested_user = SimpleWallet.objects.filter(user_id=user_id)
        serializer = WalletSerializer(requested_user,many=True)
        return Response (serializer.data) 
    if request.method == 'POST': #1. создавать, ...
        wallet_name = 'unnamed'
        if 'wallet_name' in request.data:
            wallet_name = request.data["wallet_name"]
        owner_id = User.objects.get(pk=user_id)
        new_wallet = SimpleWallet.objects.create(user_id=owner_id,wallet_name=wallet_name)
        serializer = WalletSerializer(new_wallet)
        return Response (serializer.data, status=HTTP_201_CREATED)
    elif request.method == 'PUT' or request.method =='PATCH': #редактировать...
        owner_id = User.objects.get(pk=user_id)
        wallet_id = request.data['wallet_id']
        wallet = SimpleWallet.objects.filter(user_id=owner_id).get(pk=wallet_id)
        wallet_name = request.data["wallet_name"]
        serializer = WalletSerializer(wallet,data={'wallet_name':wallet_name,'user_id':owner_id.pk})
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE': #и удалять кошелек.
        owner_id = User.objects.get(pk=user_id)
        wallet_id = request.data['wallet_id']
        wallet = SimpleWallet.objects.filter(user_id=owner_id).get(pk=wallet_id)
        wallet.delete()
        return Response(status=HTTP_204_NO_CONTENT) 

@api_view(['GET','POST','DELETE']) 
def get_transactions(request, user_id):
    if request.method == 'GET':
        if 'wallet_id' in request.data: #4. Просматривать список своих транзакций как в рамках одного кошелька,
            wallet_id=request.data['wallet_id']
            requested_transactions = Transaction.objects.filter(user_id=user_id).get(pk=wallet_id)
            serializer = TransactionSerializer(requested_transactions)
        else: #так и общий, всех кошельков сразу.
            requested_transactions = Transaction.objects.filter(user_id=user_id).order_by('wallet_id')
            serializer = TransactionSerializer(requested_transactions,many=True)
        return Response (serializer.data) 
    elif request.method == 'POST': #2. создавать
        amount = request.data['amount']
        wallet = SimpleWallet.objects.get(pk=request.data['wallet_id'])
        description = 'No transaction detail added'
        if 'description' in request.data:
            descr = request.data["description"]
        owner_id = User.objects.get(pk=user_id)
        new_transaction = Transaction.objects.create(amount_rub=amount,user_id=owner_id,wallet_id=wallet,description=descr)
        serializer = TransactionSerializer(new_transaction)
        balance = wallet.ballance_rub
        new_balance = float(balance) + float(amount)
        wallet.ballance_rub = new_balance
        wallet.save()
        return Response (serializer.data, status=HTTP_201_CREATED)
    elif request.method == 'DELETE': #и удалять транзакции в рамках кошелька 
        owner_id = User.objects.get(pk=user_id)
        transaction_id = request.data['transaction_id']
        transaction = Transaction.objects.filter(user_id=owner_id).get(pk=transaction_id)
        wallet = SimpleWallet.objects.get(pk=transaction.wallet_id.pk)
        balance = wallet.ballance_rub#transaction.wallet_id.ballance_rub
        amount = transaction.amount_rub
        transaction.delete()
        balance = wallet.ballance_rub
        new_balance = float(balance) - float(amount)
        wallet.ballance_rub = new_balance
        wallet.save()
        return Response(status=HTTP_204_NO_CONTENT) 

'''
@api_view(['GET','POST','PUT','PATCH','DELETE']) 
def get_transactions(request, user_id,wallet_id):
    if request.method == 'GET': #4. Просматривать список своих транзакций как в рамках одного кошелька
        requested_user = Transaction.objects.filter(user_id=user_id).order_by('wallet_id')
        serializer = TransactionSerializer(requested_user,many=True)
        return Response (serializer.data) 
'''