# Generated by Django 4.2.4 on 2023-08-21 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='slug',
            field=models.SlugField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(),
        ),
        migrations.AddField(
            model_name='opersystem',
            name='slug',
            field=models.SlugField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdelivery',
            name='slug',
            field=models.SlugField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderstatus',
            name='slug',
            field=models.SlugField(),
            preserve_default=False,
        ),
    ]
