from rest_framework import serializers
from apps.stock_watcher.models import StockWatch

class StockWatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockWatch
        fields = [
            'added_price',
            'current_price',
            'id',
            'pe_ratio',
            'stock_name',
            'stock_symbol',
            'suggestion',
        ]
        read_only_fields = ['id', 'current_price', 'pe_ratio', 'suggestion']

    def create(self, validated_data):
        validated_data['current_price'] = 0
        validated_data['pe_ratio'] = 0
        validated_data['suggestion'] = 'BUY'
        validated_data['user'] = self.context['request'].user
        watchlist = StockWatch.objects.create(**validated_data)
        return watchlist
