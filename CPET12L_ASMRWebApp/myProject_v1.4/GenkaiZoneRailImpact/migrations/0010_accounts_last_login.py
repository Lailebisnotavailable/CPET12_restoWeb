# Generated by Django 5.1 on 2024-10-27 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GenkaiZoneRailImpact', '0009_rename_foodid_temptransaction_food'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]