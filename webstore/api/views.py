from django.db.models.functions import Concat
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView

from shop.models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F, Q, Value, Count
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@api_view(['GET'])
def api_categories(request):
    if request.method == 'GET':
        host = request.get_host()
        categories = Category.objects.annotate(items_count=Count('item')).order_by('pk')
        for category in categories:
            category.picture_url = host + category.image.url
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def api_items(request):
    if request.method == 'GET':
        host = request.get_host()
        items = Item.objects.all().order_by('pk')
        for item in items:
            item.picture_url = host + item.image.url
            item.additional_picture_urls = []
            for additional_image in item.itemimages_set.all():
                item.additional_picture_urls.append(host + additional_image.additional_image.url)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def api_search(request):
    if request.method == 'GET':
        content = request.GET.get('content')
        host = request.get_host()
        items = Item.objects.annotate(simil=TrigramSimilarity('title', content)).filter(simil__gte=0.1)
        if not items:
            sr = SearchVector('title', 'description')
            items = Item.objects.annotate(search_vector=sr).filter(search_vector=content)
        for item in items:
            item.picture_url = host + item.image.url
            item.additional_picture_urls = []
            for additional_image in item.itemimages_set.all():
                item.additional_picture_urls.append(host + additional_image.additional_image.url)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class BrandAPIView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class OperSystemAPIView(ListAPIView):
    queryset = OperSystem.objects.all()
    serializer_class = OperSystemSerializer


class StoreReviewAPIView(ListAPIView):
    queryset = StoreReview.objects.all()
    serializer_class = StoreReviewSerializer


class ReviewAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class StoreReviewCreateAPIView(CreateAPIView):
    serializer_class = StoreReviewCreateSerializer


class ReviewCreateAPIView(CreateAPIView):
    serializer_class = ReviewCreateSerializer


class ShopCartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = ShopCart.objects.filter(buyer__user=request.user)
        serializer = ShopCartSerializer(res, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = {'buyer': request.user.buyer.pk, 'item':request.data.get('item'),
                'amount':request.data.get('amount')}
        check = ShopCart.objects.filter(buyer=data['buyer'], item=data['item'])
        if check:
            return Response({'error':'Товар уже добавлен в корзину'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ShopCartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

    def delete(self, request):
        data = {'buyer': request.user.buyer.pk, 'item':request.data.get('item')}
        check = ShopCart.objects.filter(buyer=data['buyer'], item=data['item'])
        if data['item'] == '-1':
            cart_items = ShopCart.objects.filter(buyer=data['buyer'])
            if not cart_items:
                return Response({'error':'Ваша корзина пустая'}, status = status.HTTP_400_BAD_REQUEST)
            else:
                for item in cart_items:
                    item.delete()
                return Response({'res': 'Ваша корзина успешно очищена'},status = status.HTTP_204_NO_CONTENT)
        if not check:
            return Response({'error':'Такого товара в корзине нет'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            check[0].delete()
            return Response({'res': f'Товар №{data["item"]} удален с корзины'}, status = status.HTTP_204_NO_CONTENT)


class FavoriteItemAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = FavoriteItem.objects.filter(buyer__user=request.user)
        serializer = FavoriteItemSerializer(res, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = {'buyer': request.user.buyer.pk, 'item':request.data.get('item')}
        check = FavoriteItem.objects.filter(buyer=data['buyer'], item=data['item'])
        if check:
            return Response({'error':'Товар уже добавлен в избранное'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = FavoriteItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

    def delete(self, request):
        data = {'buyer': request.user.buyer.pk, 'item':request.data.get('item')}
        check = FavoriteItem.objects.filter(buyer=data['buyer'], item=data['item'])
        if data['item'] == '-1':
            favorite_items = FavoriteItem.objects.filter(buyer=data['buyer'])
            if not favorite_items:
                return Response({'error':'Ваш список избранного пустой'}, status = status.HTTP_400_BAD_REQUEST)
            else:
                for item in favorite_items:
                    item.delete()
                return Response({'res': 'Ваш список избранного успешно очищен'},status = status.HTTP_204_NO_CONTENT)
        if not check:
            return Response({'error':'Такого товара в избранном нет'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            check[0].delete()
            return Response({'res': f'Товар №{data["item"]} удален из избранного'}, status = status.HTTP_204_NO_CONTENT)


class OrderItemAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        res = OrderItem.objects.filter(buyer=self.request.user.buyer)
        return res

    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['buyer'] = request.user.buyer.pk
        request.data._mutable = False
        return super().post(request, *args, **kwargs)




