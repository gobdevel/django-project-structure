from rest_framework import generics
from rest_framework import permissions
from apps.stock_watcher.models import Watchlist, WatchlistStock
from .serializers import (
    WatchlistSerializer,
    WatchlistStockSerializer,
    WatchlistDetailSerializer,
)


class WatchlistView(generics.ListCreateAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     """
    #     This view should return a list of all the purchases
    #     for the currently authenticated user.
    #     """
    #     user = self.request.user
    #     return Watchlist.objects.filter(user=user)


class WatchlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return Watchlist.objects.filter()


class WatchlistStockView(generics.ListCreateAPIView):
    serializer_class = WatchlistStockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        watchlist = self.kwargs.get('watchlist_id')
        return WatchlistStock.objects.filter(watchlist=watchlist)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Get URL parameter and add it to context
        context['watchlist_id'] = self.kwargs.get('watchlist_id')
        return context


class WatchlistStockDetailView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = StockWatch.objects.all()
    serializer_class = WatchlistStockSerializer
    permission_classes = [permissions.IsAuthenticated]
