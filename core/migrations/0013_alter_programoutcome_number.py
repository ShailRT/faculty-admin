# Generated by Django 4.2.7 on 2023-12-05 06:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0012_alter_customuser_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="programoutcome",
            name="number",
            field=models.IntegerField(),
        ),
    ]
