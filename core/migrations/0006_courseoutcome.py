# Generated by Django 4.2.7 on 2023-11-08 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_customuser_subjects'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseOutcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=2)),
                ('message', models.TextField()),
                ('program_outcome_priority', models.JSONField(blank=True, null=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subject')),
            ],
        ),
    ]
