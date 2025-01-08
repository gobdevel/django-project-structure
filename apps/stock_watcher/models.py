from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class StockWatch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    stock_name = models.CharField(max_length=100)
    current_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    added_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    suggestion = models.CharField(max_length=4, choices=[('BUY', 'Buy'), ('SELL', 'Sell')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock_name} ({self.stock_symbol})"
