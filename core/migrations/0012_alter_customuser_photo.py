# Generated by Django 4.2.7 on 2023-12-04 14:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_alter_courseoutcome_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="photo",
            field=models.ImageField(upload_to="faculty_profile"),
        ),
    ]
