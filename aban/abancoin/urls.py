from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy('screener'), permanent=False), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("screener",views.screener, name="screener"),
    path("coin/<str:id>", views.coin, name="coin"),
    path("buy/<str:coin_id>",views.buy, name="buy"),
]
