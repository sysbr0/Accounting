# Generated by Django 5.0.6 on 2024-07-07 10:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("biles", "0002_udsbills"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="udsbills",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_UdsBills",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
