# Generated by Django 5.1 on 2024-11-03 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GenkaiZoneRailImpact', '0013_accounts_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounts',
            name='user',
        ),
    ]
