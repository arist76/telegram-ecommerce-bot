# Generated by Django 4.2.6 on 2023-10-30 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_client', '0004_product_last_modified_product_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='click',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='notification',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='saved',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
