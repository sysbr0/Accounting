# Generated by Django 5.0.6 on 2024-08-02 19:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employe", "0012_employee_e_salary"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="balance",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
