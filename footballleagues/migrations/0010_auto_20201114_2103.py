# Generated by Django 3.1.3 on 2020-11-14 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("footballleagues", "0009_auto_20201114_1557"),
    ]

    operations = [
        migrations.AlterField(
            model_name="league",
            name="current_champion",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="current_champion",
                to="footballleagues.team",
            ),
        ),
        migrations.AlterField(
            model_name="league",
            name="most_appearances",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="most_appearances",
                to="footballleagues.player",
            ),
        ),
        migrations.AlterField(
            model_name="league",
            name="most_championships",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="most_championships",
                to="footballleagues.team",
            ),
        ),
    ]
