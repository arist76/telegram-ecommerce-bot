# Generated by Django 5.0.1 on 2024-05-28 15:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_client', '0009_productimage_count_alter_productimage_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='saved',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
