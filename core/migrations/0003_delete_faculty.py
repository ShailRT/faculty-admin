# Generated by Django 4.2.7 on 2023-11-08 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_contact_no_customuser_contact_number_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Faculty',
        ),
    ]