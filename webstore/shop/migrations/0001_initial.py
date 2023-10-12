# Generated by Django 4.2.4 on 2023-08-21 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shop.utilities


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allow_mail', models.BooleanField(default=True, verbose_name='Разрешить рассылку')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('image', models.FileField(upload_to='category/')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('edited', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('image', models.ImageField(upload_to=shop.utilities.get_path_image, verbose_name='Дополнительное изображение')),
                ('available', models.BooleanField(default=True, verbose_name='Есть в наличии')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.brand', verbose_name='Производитель')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='OperSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDelivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StoreReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('content', models.TextField(default='', verbose_name='Текст отзыва')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.buyer', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Отзыв о компании',
                'verbose_name_plural': 'Отзывы о компании',
            },
        ),
        migrations.CreateModel(
            name='ShopCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.buyer', verbose_name='Покупатель')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.item', verbose_name='Товар')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('content', models.TextField(default='')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.buyer', verbose_name='Покупатель')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.item')),
                ('to_review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.review')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.SmallIntegerField(verbose_name='Количество')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.buyer', verbose_name='Покупатель')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.orderdelivery', verbose_name='Способ доставки')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.item', verbose_name='Товар')),
                ('status', models.ForeignKey(default='в работе', on_delete=django.db.models.deletion.CASCADE, to='shop.orderstatus', verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='ItemImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_image', models.ImageField(upload_to=shop.utilities.get_path_add_image, verbose_name='Дополнительное изображение')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.item')),
            ],
            options={
                'verbose_name': 'Дополнительные изображения',
                'verbose_name_plural': 'Дополнительные изображения',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='opersystem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.opersystem'),
        ),
    ]
