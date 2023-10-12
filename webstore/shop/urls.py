from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('store_reviews/', StoreReviewCreate.as_view(), name='store_reviews'),
    path('accounts/login/', StoreLoginView.as_view(), name='login'),
    path('accounts/logout/', StoreLogoutView.as_view(), name='logout'),
    path('accounts/register/', RegisterBuyerView.as_view(), name='register'),
    path('accounts/profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('accounts/profile/reset_password/', ProfilePasswordResetView.as_view(), name='reset_password'),
    path('accounts/profile/reset_password_done/', ProfilePasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('accounts/profile/reset_password_new_password/<uidb64>/<token>/', ProfilePasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('accounts/profile/reset_password_complete/', ProfilePasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/profile/change_password/', ProfilePasswordChangeView.as_view(), name = 'password_change'),
    path('account/profile/change_password_done/', ProfilePasswordChangeDoneView.as_view(), name = 'password_change_done'),
    path('account/profile/shop_cart/', show_profile_shopcart, name = 'shop_cart'),
    path('account/profile/favorites/', FavoriteItemListView.as_view(), name = 'favorites'),
    path('account/profile/orders/', OrderItemView.as_view(), name = 'orders'),
    path('account/profile/my_reviews/', ReviewListView.as_view(), name='my_reviews'),
    path('account/profile/remove_shop_cart_item/<int:pk>/', remove_shop_cart_item, name = 'remove_shop_cart_item'),
    path('account/profile/remove_shop_cart_all/', remove_shop_cart_all, name='remove_shop_cart_all'),
    path('accounts/profile/add_shop_cart_item/<int:pk>/', to_shop_cart, name='to_shop_cart'),
    path('accounts/profile/remove_favorites/<int:pk>/', remove_from_favorites, name = 'remove_from_favorites'),
    path('accounts/profile/remove_favorites_all/', remove_from_favorites_all, name = 'remove_from_favorites_all'),
    path('catalog/', ItemsListView.as_view(), name='catalog'),
    path('about/', about_show, name = 'about'),
    path('make_order/<int:item_pk>/', OrderCreateView.as_view(), name = 'make_order'),
    path('catalog/<str:category_slug>-<int:category_pk>/', ItemsListView.as_view(), name = 'category'),
    path('detail_item/<int:pk>/<str:slug>/', ItemDetailView.as_view(), name = 'detail_item'),
    path('detail_item/<int:pk_item>/<str:slug_item>/remove_review/<int:pk>/', remove_item_review, name='remove_item_review'),
    path('accounts/profile/remove_review/<str:pk_or_all>/', remove_item_review_from_account, name='remove_item_review_from_account'),
    path('api_documentation/', api_documentation_view, name='api_documentation'),

]

