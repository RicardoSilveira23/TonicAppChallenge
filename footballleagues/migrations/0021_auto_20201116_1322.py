# Generated by Django 3.1.3 on 2020-11-16 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("footballleagues", "0020_auto_20201116_1305"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="city",
            field=models.TextField(blank=True, db_index=True),
        ),
    ]
