# Generated by Django 4.2.4 on 2023-08-21 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_brand_slug_alter_item_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(),
        ),
        migrations.AlterField(
            model_name='opersystem',
            name='slug',
            field=models.SlugField(),
        ),
        migrations.AlterField(
            model_name='orderdelivery',
            name='slug',
            field=models.SlugField(),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='slug',
            field=models.SlugField(),
        ),
    ]
