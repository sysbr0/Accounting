# Generated by Django 5.0.6 on 2024-07-04 21:00

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Costomers",
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
                ("name", models.TextField()),
                ("image", models.URLField(blank=True, null=True)),
                ("tex", models.IntegerField(blank=True, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("number", models.CharField(max_length=255)),
                ("is_company", models.BooleanField()),
                ("company", models.TextField(blank=True, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                (
                    "token",
                    models.CharField(default=uuid.uuid4, max_length=36, unique=True),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_customers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]