# Generated by Django 4.2.4 on 2023-08-29 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_shopcart_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoriteitem',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='orderdelivery',
            options={'verbose_name': 'Способ доставки', 'verbose_name_plural': 'Способ доставки'},
        ),
        migrations.AlterModelOptions(
            name='orderstatus',
            options={'verbose_name': 'Статус заказа', 'verbose_name_plural': 'Статус заказа'},
        ),
        migrations.AlterModelOptions(
            name='shopcart',
            options={'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзина'},
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.orderstatus', verbose_name='Статус'),
        ),
    ]