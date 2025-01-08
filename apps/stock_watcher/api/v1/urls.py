from django.urls import path
from .views import StockWatchList, StockWatchDetail


urlpatterns = [
    path("", StockWatchList.as_view(), name='watch-list'),
    path("<int:pk>/", StockWatchDetail.as_view(), name='watch-list-detail'),
]