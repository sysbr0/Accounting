# Generated by Django 5.0.6 on 2024-07-10 07:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employe", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employee",
            name="title",
        ),
        migrations.AlterField(
            model_name="employee",
            name="tc",
            field=models.CharField(blank=True, max_length=11, null=True, unique=True),
        ),
    ]
