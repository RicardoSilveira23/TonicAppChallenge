# Generated by Django 3.1.3 on 2020-11-16 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("footballleagues", "0015_auto_20201116_1247"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="name",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]