# Generated by Django 5.0.6 on 2024-07-10 08:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employe", "0003_employee_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="state",
            field=models.BooleanField(default=True),
        ),
    ]