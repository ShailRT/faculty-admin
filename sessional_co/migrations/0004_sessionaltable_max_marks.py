# Generated by Django 4.2.7 on 2024-04-04 00:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sessional_co", "0003_sessionaltable_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="sessionaltable",
            name="max_marks",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
