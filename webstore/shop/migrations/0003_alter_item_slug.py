# Generated by Django 4.2.4 on 2023-08-21 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_brand_slug_category_slug_item_slug_opersystem_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='s'),
        ),
    ]