from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse

from .utilities import *

# Create your models here.

class Brand(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производитель'
        ordering = ['title']

class OperSystem(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Операционная система'
        verbose_name_plural = 'Операционная система'
        ordering = ['title']


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    image = models.FileField(upload_to='category/')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug' : self.slug, 'category_pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['pk']


class Item (models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    opersystem = models.ForeignKey(OperSystem, on_delete=models.PROTECT, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name="Производитель")
    price = models.IntegerField(verbose_name='Цена')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    edited = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    image = models.ImageField(upload_to=get_path_image, verbose_name='Изображение')
    available = models.BooleanField(default=True, verbose_name='Есть в наличии')
    slug = models.SlugField()

    def clean(self):
        errors = {}
        if self.category.title in ['Телефоны', "Планшеты", "Ноутбуки", "Приставки", "Персональные компьюторы"]:
            if self.opersystem is None:
                errors['opersystem']=[ValidationError('Вы не выбрали операционную систему устройства')]
        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse('detail_item', kwargs={'pk': self.pk, 'slug' : self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-available', 'pk']


class ItemImages(models.Model):
    additional_image = models.ImageField(upload_to=get_path_add_image,verbose_name='Дополнительное изображение')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        verbose_name='Дополнительные изображения'
        verbose_name_plural = 'Дополнительные изображения'


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    allow_mail = models.BooleanField(default=True, verbose_name='Разрешить рассылку')

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class ShopCart(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT, verbose_name='Покупатель')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name='Товар')
    amount = models.SmallIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        ordering = ['-pk']


class FavoriteItem(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT, verbose_name = 'Покупатель')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name = 'Товар')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['-pk']


class OrderStatus(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статус заказа'

    def __str__(self):
        return self.title


class OrderDelivery(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способ доставки'


class OrderItem(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT, verbose_name='Покупатель')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name='Товар')
    amount = models.SmallIntegerField(verbose_name='Количество')
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, default=2, verbose_name='Статус')
    delivery = models.ForeignKey(OrderDelivery, on_delete=models.PROTECT, verbose_name='Способ доставки')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    comment = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def total_price(self):
        return self.item.price * self.amount

    def __str__(self):
        return f'{self.item.title}-{self.created.strftime("%d.%m.%Y в %H:%M")}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-pk']


class StoreReview(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Покупатель')
    name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(verbose_name='Электронная почта')
    content = models.TextField(verbose_name='Текст отзыва')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Отзыв о компании'
        verbose_name_plural = 'Отзывы о компании'
        ordering = ['-pk']

    def __str__(self):
        return f'{self.name} - {self.created.strftime("%d.%m.%Y в %H:%M")}'


class Review(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Покупатель')
    name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(verbose_name='Электронная почта')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    to_review = models.ForeignKey('self', on_delete= models.CASCADE, blank=True, null=True, related_name='child')
    content = models.TextField(default='', verbose_name='Текст отзыва')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return f'{self.name} - {self.created.strftime("%d.%m.%Y в %H:%M")}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pk']





