# Generated by Django 5.0.1 on 2024-05-27 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_client', '0007_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='detailed_description',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller_chat',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller_details',
            field=models.TextField(blank=True, null=True),
        ),
    ]