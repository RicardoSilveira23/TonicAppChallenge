# Generated by Django 3.1.3 on 2020-11-14 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("footballleagues", "0005_auto_20201113_2056"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="player",
            index=models.Index(fields=["name"], name="footballlea_name_e0ada8_idx"),
        ),
    ]
