# Generated by Django 4.2.5 on 2023-10-03 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_alter_product_price_alter_product_quantity"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="created_at",
        ),
    ]
