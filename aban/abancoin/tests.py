from django.test import TestCase
from django.contrib.auth.models import User
from .models import Coin

class CoinModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.coin = Coin.objects.create(user=self.user, name='aban', quantity=5, price=50000)

    def test_coin_creation(self):
        coin = Coin.objects.get(name='aban')
        self.assertEqual(coin.quantity, 5)
        self.assertEqual(coin.price, 50000)
        self.assertEqual(coin.user, self.user)

    def test_coin_str(self):
        coin = Coin.objects.get(name='aban')
        self.assertEqual(str(coin), 'aban - 5')
