# -----------------------------------------------------------------------------
# Copyright (c) 2025 Tekyonix
# All rights reserved.
#
#
# Licensed under the MIT License.
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
#
# -----------------------------------------------------------------------------

import random
from factory.django import DjangoModelFactory
from factory import SubFactory, Faker

from common.constants import Suggestions


class WatchlistFactory(DjangoModelFactory):
    class Meta:
        model = 'stock_watcher.Watchlist'

    user = SubFactory('apps.users.tests.factories.custom_user.CustomUserFactory')
    name = Faker('name')
    currency = 1
    created_at = Faker('date_time_this_month')


class WatchlistStockFactory(DjangoModelFactory):
    class Meta:
        model = 'stock_watcher.WatchlistStock'

    watchlist = SubFactory(WatchlistFactory)
    symbol = Faker('name')
    name = Faker('name')
    current_price = Faker('pydecimal', left_digits=3, right_digits=2)
    added_price = Faker('pydecimal', left_digits=3, right_digits=2)
    pe_ratio = Faker('pydecimal', left_digits=2, right_digits=2)
    suggestion = random.choice(Suggestions.values())
    created_at = Faker('date_time_this_month')
    updated_at = Faker('date_time_this_month')
