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

from django.urls import path
from .views import (
    WatchlistView,
    WatchlistDetailView,
    WatchlistStockView,
    WatchlistStockDetailView,
)

urlpatterns = [
    path("", WatchlistView.as_view(), name='watchlist'),
    path("<int:pk>/", WatchlistDetailView.as_view(), name='watchlist-detail'),
    path(
        "<int:watchlist_id>/stocks/",
        WatchlistStockView.as_view(),
        name='watchlist-stocks',
    ),
    path(
        "<int:watchlist_id>/stocks/<int:pk>/",
        WatchlistStockDetailView.as_view(),
        name='watchlist-stock-detail',
    ),
]
