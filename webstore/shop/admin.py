from django.contrib import admin
from .models import *
from django.contrib.admin import StackedInline

# Register your models here.

class ItemImagesInline(StackedInline):
    model = ItemImages

class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemImagesInline]
    exclude = ('created',)
    prepopulated_fields = {'slug':['title']}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}


class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


class OrderDeliveryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


class OrderStatusAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


class OperSystemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


admin.site.register(Item, ItemAdmin)
admin.site.register(StoreReview)
admin.site.register(Buyer)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(OperSystem, OperSystemAdmin)
admin.site.register(Review)
admin.site.register(FavoriteItem)
admin.site.register(OrderStatus, OrderStatusAdmin)
admin.site.register(OrderDelivery, OrderDeliveryAdmin)
admin.site.register(ShopCart)
admin.site.register(OrderItem)



