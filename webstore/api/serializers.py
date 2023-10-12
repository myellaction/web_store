from django.http import HttpRequest
from rest_framework import serializers
from shop.models import *
from pprint import pprint


class CategorySerializer(serializers.ModelSerializer):
    picture_url = serializers.URLField(default=None)
    items_count = serializers.IntegerField()
    class Meta:
        model = Category
        fields = ('id', 'title', 'picture_url', 'items_count', 'slug')


class ItemSerializer(serializers.ModelSerializer):
    picture_url = serializers.URLField(default=None)
    additional_picture_urls = serializers.ListField(default=None)
    class Meta:
        model = Item
        fields = ('id', 'title', 'category', 'description', 'opersystem', 'brand', 'price',
                  'created', 'edited', 'picture_url', 'additional_picture_urls', 'available', 'slug')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'title')


class OperSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperSystem
        fields = ('id', 'title')


class StoreReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreReview
        fields = ('id', 'name', 'content', 'created')


class StoreReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreReview
        fields = ('name', 'email', 'content')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'name', 'content', 'item', 'created')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'name', 'email', 'content', 'item')


class ShopCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopCart
        fields = ('id', 'buyer', 'item', 'amount')


class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = ('id', 'buyer', 'item')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        comment = serializers.CharField(max_length=2000, required=False)
        model = OrderItem
        fields = ('buyer', 'item', 'amount', 'delivery', 'address', 'comment')
