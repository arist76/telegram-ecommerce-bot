# Generated by Django 5.0.1 on 2024-05-26 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_client', '0006_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.IntegerField(unique=True),
        ),
    ]
