# Generated by Django 4.2.7 on 2024-02-16 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0003_alter_category_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="subcategory",
            name="parent",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="post.subcategory"
            ),
        ),
    ]
