# Generated by Django 5.0.6 on 2024-07-10 10:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employe", "0004_employee_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="status",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
