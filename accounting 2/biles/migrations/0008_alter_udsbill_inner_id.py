# Generated by Django 5.0.6 on 2024-07-08 20:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("biles", "0007_udsbills_net_udsbills_top"),
    ]

    operations = [
        migrations.AlterField(
            model_name="udsbill_inner",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]