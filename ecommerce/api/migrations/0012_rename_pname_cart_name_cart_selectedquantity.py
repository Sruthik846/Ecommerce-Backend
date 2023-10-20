# Generated by Django 4.2.5 on 2023-10-20 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0011_cart_delete_productimages"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cart",
            old_name="pname",
            new_name="name",
        ),
        migrations.AddField(
            model_name="cart",
            name="selectedQuantity",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
