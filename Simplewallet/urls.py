from django.contrib import admin
from django.urls import path
from swallet import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wallets/<str:user_id>',views.get_wallets),    
    #path('transactions/<str:user_id>/<int:wallet_id>/',views.get_wallets),
    path('transactions/<str:user_id>',views.get_transactions),

]