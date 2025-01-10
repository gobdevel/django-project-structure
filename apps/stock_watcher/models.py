# -----------------------------------------------------------------------------
# Copyright (c) 2025 [Your Name or Your Organization]
# All rights reserved.
#
# This file is part of Watcher.
#
# Licensed under the MIT License.
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
#
# -----------------------------------------------------------------------------

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

from common.constants import Currency, Suggestions


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    currency = models.IntegerField(choices=Currency.choices(), default=Currency.USD)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'name']

    def get_currency_label(self):
        return Currency(self.currency).name.upper()

    def __str__(self):
        return self.name


class WatchlistStock(models.Model):
    watchlist = models.ForeignKey(
        Watchlist, related_name="stocks", on_delete=models.CASCADE
    )
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    current_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))]
    )
    added_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))]
    )
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    suggestion = models.IntegerField(
        choices=Suggestions.choices(), default=Suggestions.NONE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['watchlist', 'symbol']

    def __str__(self):
        return self.symbol

    def get_suggestion_label(self):
        return Suggestions(self.suggestion).name.upper()
