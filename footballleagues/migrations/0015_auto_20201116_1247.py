# Generated by Django 3.1.3 on 2020-11-16 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("footballleagues", "0014_auto_20201115_2257"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="player",
            index=models.Index(fields=["name"], name="player_name_idx"),
        ),
    ]
