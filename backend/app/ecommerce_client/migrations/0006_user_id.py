# Generated by Django 5.0.1 on 2024-05-26 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_client', '0005_remove_product_posted_product_posted_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id',
            field=models.CharField(default=0, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
