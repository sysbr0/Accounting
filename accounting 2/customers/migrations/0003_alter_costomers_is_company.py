# Generated by Django 5.0.6 on 2024-07-08 14:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0002_alter_costomers_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="costomers",
            name="is_company",
            field=models.BooleanField(default=0),
        ),
    ]
