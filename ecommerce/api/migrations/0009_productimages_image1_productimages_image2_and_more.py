# Generated by Django 4.2.5 on 2023-10-16 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_productimages"),
    ]

    operations = [
        migrations.AddField(
            model_name="productimages",
            name="image1",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
        migrations.AddField(
            model_name="productimages",
            name="image2",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
        migrations.AddField(
            model_name="productimages",
            name="image3",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
        migrations.AddField(
            model_name="productimages",
            name="image4",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
