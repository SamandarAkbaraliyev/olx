# Generated by Django 4.2.7 on 2024-02-16 10:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0004_subcategory_parent"),
    ]

    operations = [
        migrations.AddField(
            model_name="subcategory",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
    ]
