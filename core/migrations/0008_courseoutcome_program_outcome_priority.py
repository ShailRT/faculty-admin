# Generated by Django 4.2.7 on 2023-11-08 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_courseoutcome_program_outcome_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseoutcome',
            name='program_outcome_priority',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
