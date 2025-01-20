from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from apps.stock_watcher.models import Watchlist, WatchlistStock
from apps.users.api.v1.serializers import UserSerializer
from apps.users.models import CustomUser


class WatchlistStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchlistStock
        fields = [
            'id',
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
            'created_at',
            'updated_at',
            'current_price',
            'pe_ratio',
            'suggestion',
        ]

    def validate(self, data):
        watchlist_id = self.context['watchlist_id']
        # Ensure watchlist exists
        try:
            watchlist = Watchlist.objects.get(id=watchlist_id)
            data['watchlist'] = watchlist
        except Watchlist.DoesNotExist:
            raise serializers.ValidationError('Invalid watchlist')

        if watchlist.user != self.context['request'].user:
            raise serializers.ValidationError('Invalid watchlist')
        return data

    def create(self, validated_data):
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
        read_only_fields = ['id', 'created_at', 'stocks']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        try:
            watchlist = Watchlist.objects.create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(e)

        return watchlist

    def update(self, instance, validated_data):
        if instance.user != self.context['request'].user:
            raise serializers.ValidationError('Invalid watchlist')
        return super().update(instance, validated_data)


class WatchlistDetailSerializer(serializers.ModelSerializer):
    stocks = WatchlistStockSerializer(many=True, read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'name', 'currency', 'created_at', 'stocks']
        read_only_fields = ['id', 'created_at']

    def update(self, instance, validated_data):
        if instance.user != self.context['request'].user:
            raise serializers.ValidationError('Invalid watchlist')
        return super().update(instance, validated_data)
