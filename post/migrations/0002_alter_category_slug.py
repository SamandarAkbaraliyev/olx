# Generated by Django 4.2.7 on 2024-02-16 06:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(blank=True, editable=False, null=True),
        ),
    ]