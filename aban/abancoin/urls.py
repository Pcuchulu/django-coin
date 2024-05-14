from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('screener/', views.screener, name='screener'),
    path('buy/', views.buy, name='buy'),
    path('cash/', views.cash, name='cash'),
    path('holdings/', views.holdings, name='holdings'),
    path('sell/', views.sell, name='sell'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
]
