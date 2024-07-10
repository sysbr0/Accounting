# Generated by Django 5.0.6 on 2024-07-07 19:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_rename_first_name_customuser_full_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="profile_image",
            field=models.ImageField(blank=True, null=True, upload_to="profile_images/"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="tax_number",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
