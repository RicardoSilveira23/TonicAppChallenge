# Generated by Django 3.1.3 on 2020-11-13 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("footballleagues", "0002_auto_20201112_1551"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="coach",
            field=models.TextField(blank=True),
        ),
    ]
