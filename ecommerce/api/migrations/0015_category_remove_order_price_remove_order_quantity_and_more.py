# Generated by Django 4.1.4 on 2023-11-16 04:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0014_orderupdates"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("category", models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="order",
            name="price",
        ),
        migrations.RemoveField(
            model_name="order",
            name="quantity",
        ),
        migrations.RemoveField(
            model_name="order",
            name="total",
        ),
        migrations.AddField(
            model_name="order",
            name="order_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="order",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.cart"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="category_product",
                to="api.category",
            ),
        ),
    ]