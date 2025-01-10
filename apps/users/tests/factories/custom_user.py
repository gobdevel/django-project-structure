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
from factory import Faker


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = 'users.CustomUser'

    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    is_staff = False
    is_active = True
    # created_at = Faker('date_time_this_year')
