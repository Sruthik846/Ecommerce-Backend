# Generated by Django 4.2.5 on 2023-11-03 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0012_rename_pname_cart_name_cart_selectedquantity"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order_number", models.CharField(max_length=100, unique=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Received", "Received"),
                            ("Scheduled", "Scheduled"),
                            ("Shipped", "Shipped"),
                            ("In Progress", "In Progress"),
                        ],
                        max_length=20,
                    ),
                ),
                ("product", models.CharField(max_length=50, null=True)),
                ("quantity", models.CharField(max_length=50, null=True)),
                ("price", models.CharField(max_length=50, null=True)),
                ("total", models.CharField(max_length=500, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.userdetails",
                    ),
                ),
            ],
        ),
    ]
