# Generated by Django 4.2.4 on 2023-09-01 08:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_alter_item_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 1, 8, 56, 33, 16532, tzinfo=datetime.timezone.utc), verbose_name='Дата добавления'),
        ),
    ]
