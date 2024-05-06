import json
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import requests
from django.shortcuts import render

from abancoin.models import User, Coin

# Create your views here.


def login_view(request):
    if request.method == "POST":

        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "abancoin/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "abancoin/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "abancoin/register.html", {
                "message": "Passwords must match."
            })

        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "abancoin/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("screener"))
    else:
        return render(request, "abancoin/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("screener"))

def dashboard(request):
    return render(request, "abancoin/dashboard.html")

def screener(request):
    if request.user.is_authenticated:
        holdings = Coin.objects.filter(user=request.user)
        userdata = User.objects.get(id=request.user.id)
        abancoin_price = 4.0
        abancoin_quantity = 0  
        return render(request, "abancoin/dashboard.html", {
            'abancoin_price': abancoin_price,
            'abancoin_quantity': abancoin_quantity,
            'userdata': userdata,
            'holdings': holdings
        })
    else:
        # Redirect to login page if user is not authenticated
        return HttpResponseRedirect(reverse("login"))


@login_required
def buy(request):
    if request.method == "POST":
        
        coin_name = request.POST.get("coin_name", "")  
        quantity = float(request.POST.get("quantity", 0))  

        
        coin_prices = {
            "abancoin": 4.0,    
        }

        
        if coin_name in coin_prices and quantity > 0:
            price = coin_prices[coin_name]
            total_cost = price * quantity

            
            if total_cost < 10:
                aggregated_orders = request.session.get("aggregated_orders", [])
                if aggregated_orders and aggregated_orders[0]["coin_name"] == coin_name:
                    aggregated_orders[0]["quantity"] += quantity
                    aggregated_orders[0]["total_cost"] += total_cost
                else:
                    aggregated_order = {
                        "coin_name": coin_name,
                        "quantity": quantity,
                        "total_cost": total_cost
                    }
                    aggregated_orders.insert(0, aggregated_order)
                request.session["aggregated_orders"] = aggregated_orders
                return render(request, "VSCrypto/dashboard.html", {
                    'message': f"Order for {coin_name} has been added to aggregation",
                })
            else:

                curbalance = User.objects.get(username=request.user.username).balance
                if total_cost <= curbalance:
                    
                    curbalance -= total_cost
                    User.objects.filter(username=request.user.username).update(balance=curbalance)

                    
                    buy_from_exchange(coin_name, quantity)

                    
                    print("TRANSACTION COMPLETE")
                    userdata = User.objects.get(id=request.user.id)
                    holdings = Coin.objects.filter(user=request.user)
                    return render(request, "VSCrypto/dashboard.html", {
                        'message': "Transaction Complete",
                        'userdata': userdata,
                        'holdings': holdings
                    })
                else:
                    print("NOT ENOUGH BALANCE")
                    userdata = User.objects.get(id=request.user.id)
                    holdings = Coin.objects.filter(user=request.user)
                    return render(request, "VSCrypto/dashboard.html", {
                        'message': "Transaction Failed: Not enough balance",
                        'userdata': userdata,
                        'holdings': holdings
                    })
        else:
            print("INVALID COIN NAME OR QUANTITY")
            userdata = User.objects.get(id=request.user.id)
            holdings = Coin.objects.filter(user=request.user)
            return render(request, "VSCrypto/dashboard.html", {
                'message': "Invalid coin name or quantity",
                'userdata': userdata,
                'holdings': holdings
            })
    else:
        pass


@login_required
def cash(request):
    userdata = User.objects.get(id=request.user.id)
    return render(request, "abancoin/cash.html",{
        'nums':list(range(0, 14)),
        'userdata':userdata,
    })

@login_required
def holdings(request):
    holdings = Coin.objects.filter(user = request.user)
    return render(request, "abancoin/holdings.html",{
        'nums':list(range(0, 14)),
        'holdings':holdings
    })

@login_required
def sell(request ,id , price ,qty):



@login_required
def deposit(request):

@login_required
def withdraw(request):

@login_required
def buy_from_exchange(coin_name, quantity):
    pass


    