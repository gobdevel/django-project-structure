from rest_framework import generics
from rest_framework import permissions
from apps.stock_watcher.models import StockWatch
from .serializers import StockWatchSerializer

class StockWatchList(generics.ListCreateAPIView):
    queryset = StockWatch.objects.all()
    serializer_class = StockWatchSerializer
    permission_classes = [permissions.IsAuthenticated]


class StockWatchDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockWatch.objects.all()
    serializer_class = StockWatchSerializer
    permission_classes = [permissions.IsAuthenticated]
