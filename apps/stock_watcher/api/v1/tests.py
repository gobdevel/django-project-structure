from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.stock_watcher.models import StockWatch

CustomUser = get_user_model()

class StockWatchAPITest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@gmail.com', password='12345')
        self.client.login(email='testuser@gmail.com', password='12345')
        self.stock_watch = StockWatch.objects.create(
            user=self.user,
            stock_symbol='AAPL',
            stock_name='Apple Inc.',
            current_price=150.00,
            added_price=145.00,
            pe_ratio=30.00,
            suggestion='BUY'
        )
        self.list_url = reverse('watch-list')
        self.detail_url = reverse('watch-list-detail', args=[self.stock_watch.id])

    def test_get_stock_watchlist(self):
        response = self.client.get(self.list_url, {'ordering': 'created_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 1)
        self.assertEqual(response.data['results'][0]['stock_symbol'], 'AAPL')

    def test_get_stock_watch_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stock_symbol'], 'AAPL')

    def test_create_stock_watch(self):
        data = {
            'user': self.user.id,
            'stock_symbol': 'GOOGL',
            'stock_name': 'Alphabet Inc.',
            'current_price': 2800.00,
            'added_price': 2750.00,
            'pe_ratio': 35.00,
            'suggestion': 'BUY'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['stock_symbol'], 'GOOGL')

    def test_update_stock_watch(self):
        data = {
            'user': self.user.id,
            'stock_symbol': 'AAPL',
            'stock_name': 'Apple Inc.',
            'current_price': 155.00,
            'added_price': 145.00,
            'pe_ratio': 32.00,
            'suggestion': 'SELL'
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_price'], '155.00')
        self.assertEqual(response.data['suggestion'], 'SELL')

    def test_delete_stock_watch(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(StockWatch.objects.count(), 0)

    def test_create_stock_watch_invalid_suggestion(self):
        data = {
            'user': self.user.id,
            'stock_symbol': 'GOOGL',
            'stock_name': 'Alphabet Inc.',
            'current_price': 2800.00,
            'added_price': 2750.00,
            'pe_ratio': 35.00,
            'suggestion': 'HOLD'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_stock_watch_negative_price(self):
        data = {
            'user': self.user.id,
            'stock_symbol': 'GOOGL',
            'stock_name': 'Alphabet Inc.',
            'current_price': -2800.00,
            'added_price': 2750.00,
            'pe_ratio': 35.00,
            'suggestion': 'BUY'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)