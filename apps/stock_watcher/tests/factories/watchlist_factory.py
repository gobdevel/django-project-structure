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

from factory.django import DjangoModelFactory
from factory import SubFactory, Faker


class WatchlistFactory(DjangoModelFactory):
    class Meta:
        model = 'stock_watcher.Watchlist'

    user = SubFactory('apps.users.tests.factories.user_factory.UserFactory')
    name = Faker('name')
    currency = 1
    created_at = Faker('date_time_this_month')
