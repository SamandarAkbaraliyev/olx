# Generated by Django 4.2.7 on 2024-02-16 12:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0010_region_category_has_exchange_category_has_free_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="published_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]