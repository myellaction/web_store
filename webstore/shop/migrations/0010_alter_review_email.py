# Generated by Django 4.2.4 on 2023-08-24 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_review_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Электронная почта'),
        ),
    ]