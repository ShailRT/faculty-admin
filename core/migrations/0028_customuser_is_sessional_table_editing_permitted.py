# Generated by Django 4.2.7 on 2024-03-31 23:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0027_accessrequest_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_sessional_table_editing_permitted",
            field=models.BooleanField(default=False),
        ),
    ]
