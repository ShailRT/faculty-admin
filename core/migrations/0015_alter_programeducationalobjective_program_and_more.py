# Generated by Django 4.2.7 on 2023-12-05 06:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_programeducationalobjective"),
    ]

    operations = [
        migrations.AlterField(
            model_name="programeducationalobjective",
            name="program",
            field=models.CharField(choices=[("B.Tech", "B.Tech")], max_length=120),
        ),
        migrations.AlterField(
            model_name="programoutcome",
            name="program",
            field=models.CharField(choices=[("B.Tech", "B.Tech")], max_length=120),
        ),
    ]