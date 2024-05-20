# Generated by Django 4.2.7 on 2024-05-16 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exit_survey', '0002_remove_exitsurvey_students'),
        ('sessional_co', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessionaltable',
            name='student_info',
        ),
        migrations.AlterField(
            model_name='sessionaltable',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exit_survey.sessionstudent'),
        ),
    ]