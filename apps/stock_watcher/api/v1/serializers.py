from rest_framework import serializers
from apps.stock_watcher.models import Watchlist, WatchlistStock


class WatchlistStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchlistStock
        fields = [
            'id',
            'watchlist',
            'symbol',
            'name',
            'current_price',
            'added_price',
            'pe_ratio',
            'suggestion',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'watchlist',
            'created_at',
            'updated_at',
            'current_price',
            'pe_ratio',
            'suggestion',
        ]

    def create(self, validated_data):
        request_object = self.context['request']
        watchlist_id = self.context['watchlist_id']
        if watchlist_id is None:
            raise serializers.ValidationError('watchlist is none')
        watchlist = Watchlist.objects.get(id=watchlist_id)
        if watchlist.user != request_object.user:
            raise serializers.ValidationError('Invalid watchlist')
        validated_data['watchlist'] = watchlist
        validated_data['current_price'] = 0
        validated_data['pe_ratio'] = 0
        validated_data['suggestion'] = 0
        stock = WatchlistStock.objects.create(**validated_data)
        return stock

    def update(self, instance, validated_data):
        watchlist = validated_data.get('watchlist')
        if watchlist and watchlist.user != self.context['request'].user:
            raise serializers.ValidationError('Invalid watchlist')
        return super().update(instance, validated_data)


class WatchlistSerializer(serializers.ModelSerializer):
    stocks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'name', 'currency', 'created_at', 'stocks']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        watchlist = Watchlist.objects.create(**validated_data)
        return watchlist


class WatchlistDetailSerializer(serializers.ModelSerializer):
    stocks = WatchlistStockSerializer(many=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'name', 'currency', 'created_at', 'stocks']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        watchlist = Watchlist.objects.create(**validated_data)
        return watchlist
