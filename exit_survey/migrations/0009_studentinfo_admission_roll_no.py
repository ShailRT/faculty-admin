# Generated by Django 4.2.7 on 2024-11-21 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exit_survey', '0008_alter_studentinfo_co_response_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinfo',
            name='admission_roll_no',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
