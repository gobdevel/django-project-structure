from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# from .models import StockWatchA
from apps.stock_watcher.models import StockWatch

class StockWatchModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@gmail.com',
            password='12345'
        )
        self.stock_watch = StockWatch.objects.create(
            user=self.user,
            stock_symbol='AAPL',
            stock_name='Apple Inc.',
            current_price=150.00,
            added_price=145.00,
            pe_ratio=30.00,
            suggestion='BUY'
        )

    def test_stock_watch_creation(self):
        self.assertEqual(self.stock_watch.user.email, 'testuser@gmail.com')
        self.assertEqual(self.stock_watch.stock_symbol, 'AAPL')
        self.assertEqual(self.stock_watch.stock_name, 'Apple Inc.')
        self.assertEqual(self.stock_watch.current_price, 150.00)
        self.assertEqual(self.stock_watch.added_price, 145.00)
        self.assertEqual(self.stock_watch.pe_ratio, 30.00)
        self.assertEqual(self.stock_watch.suggestion, 'BUY')

    def test_stock_watch_str(self):
        self.assertEqual(str(self.stock_watch), 'Apple Inc. (AAPL)')

    def test_stock_symbol_max_length(self):
        stock_watch = StockWatch.objects.create(
            user=self.user,
            stock_symbol='A' * 10,
            stock_name='Test Stock',
            current_price=100.00,
            added_price=95.00,
            pe_ratio=20.00,
            suggestion='BUY'
        )
        self.assertEqual(stock_watch.stock_symbol, 'A' * 10)

    def test_stock_symbol_exceeds_max_length(self):
        with self.assertRaises(ValidationError):
            stock_watch = StockWatch(
                user=self.user,
                stock_symbol='A' * 11,
                stock_name='Test Stock',
                current_price=100.00,
                added_price=95.00,
                pe_ratio=20.00,
                suggestion='BUY'
            )
            stock_watch.full_clean()

    def test_invalid_suggestion(self):
        with self.assertRaises(ValidationError):
            stock_watch = StockWatch(
                user=self.user,
                stock_symbol='AAPL',
                stock_name='Apple Inc.',
                current_price=150.00,
                added_price=145.00,
                pe_ratio=30.00,
                suggestion='HOLD'
            )
            stock_watch.full_clean()

    def test_negative_current_price(self):
        with self.assertRaises(ValidationError):
            stock_watch = StockWatch(
                user=self.user,
                stock_symbol='AAPL',
                stock_name='Apple Inc.',
                current_price=-150.00,
                added_price=145.00,
                pe_ratio=30.00,
                suggestion='BUY'
            )
            stock_watch.full_clean()

    def test_negative_added_price(self):
        with self.assertRaises(ValidationError):
            stock_watch = StockWatch(
                user=self.user,
                stock_symbol='AAPL',
                stock_name='Apple Inc.',
                current_price=150.00,
                added_price=-145.00,
                pe_ratio=30.00,
                suggestion='BUY'
            )
            stock_watch.full_clean()
