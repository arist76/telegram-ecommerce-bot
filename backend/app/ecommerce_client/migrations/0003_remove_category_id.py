# Generated by Django 5.0.1 on 2024-05-26 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_client', '0002_productimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='id',
        ),
    ]
