# Generated by Django 4.2.7 on 2023-11-06 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='contact_no',
            new_name='contact_number',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='college_faculty_email',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='date_created',
        ),
    ]
