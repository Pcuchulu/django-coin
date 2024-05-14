from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Coin
from .serializers import CoinSerializer
from django.db import transaction

@api_view(['POST'])
def login_view(request):
    if request.method == "POST":
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"})
        else:
            return Response({"message": "Invalid username and/or password"}, status=400)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"message": "Logout successful"})

@api_view(['POST'])
def register(request):
    if request.method == "POST":
        username = request.data.get("username", "")
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        confirmation = request.data.get("confirmation", "")

        if password != confirmation:
            return Response({"message": "Passwords must match"}, status=400)

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return Response({"message": "Registration successful"})
        except IntegrityError:
            return Response({"message": "Username already taken"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    return Response({"message": "Dashboard data goes here"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def screener(request):
    holdings = Coin.objects.filter(user=request.user)
    userdata = request.user
    abancoin_price = 4.0
    abancoin_quantity = 0
    serializer = CoinSerializer(holdings, many=True)
    return Response({
        'abancoin_price': abancoin_price,
        'abancoin_quantity': abancoin_quantity,
        'userdata': userdata,
        'holdings': serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy(request):
    if request.method == "POST":
        coin_name = request.data.get("coin_name", "")
        quantity = float(request.data.get("quantity", 0))

        coin_prices = {
            "abancoin": 4.0,
            # Add other coin prices here
        }

        if coin_name in coin_prices and quantity > 0:
            price = coin_prices[coin_name]
            total_cost = price * quantity

            with transaction.atomic():
                try:
                    user = request.user
                    cur_balance = user.balance
                    if total_cost <= cur_balance:
                        # Deduct the total cost from user's balance
                        cur_balance -= total_cost
                        user.balance = cur_balance
                        user.save()

                        # Perform other operations such as creating the coin object
                        Coin.objects.create(user=user, name=coin_name, quantity=quantity, price=price)

                        # Return success response
                        return Response({"message": "Transaction successful"})
                    else:
                        return Response({"message": "Not enough balance"}, status=400)
                except Exception as e:
                    # Rollback the transaction if an exception occurs
                    return Response({"message": f"Transaction failed: {str(e)}"}, status=400)
        else:
            return Response({"message": "Invalid coin name or quantity"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cash(request):
    userdata = request.user
    return Response({"message": "Cash endpoint"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def holdings(request):
    holdings = Coin.objects.filter(user=request.user)
    serializer = CoinSerializer(holdings, many=True)
    return Response({"message": "Holdings endpoint", "holdings": serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sell(request):
    # Implement the sell logic here
    return Response({"message": "Sell endpoint"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request):
    # Implement the deposit logic here
    return Response({"message": "Deposit endpoint"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw(request):
    # Implement the withdraw logic here
    return Response({"message": "Withdraw endpoint"})