# Generated by Django 4.1.4 on 2023-11-16 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_category_remove_order_price_remove_order_quantity_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
