# Generated by Django 5.0.6 on 2024-07-07 19:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_customuser_profile_image_customuser_tax_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="company",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="company_tr",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]