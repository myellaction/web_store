from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView



urlpatterns = [
    path('categories/', api_categories),
    path('items/', api_items),
    path('search_item/', api_search),
    path('brands/', BrandAPIView.as_view()),
    path('oper_systems/', OperSystemAPIView.as_view()),
    path('store_reviews/', StoreReviewAPIView.as_view()),
    path('store_reviews/create/', StoreReviewCreateAPIView.as_view()),
    path('reviews/', ReviewAPIView.as_view()),
    path('reviews/create/', ReviewCreateAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('shop_cart/', ShopCartAPIView.as_view()),
    path('favorite_item/', FavoriteItemAPIView.as_view()),
    path('order_item/', OrderItemAPIView.as_view()),

]



# сделать заказ - для авторизированных пользователей



