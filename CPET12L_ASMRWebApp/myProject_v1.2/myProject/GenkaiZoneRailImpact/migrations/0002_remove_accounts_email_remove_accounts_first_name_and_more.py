# Generated by Django 5.1 on 2024-10-14 07:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GenkaiZoneRailImpact', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounts',
            name='email',
        ),
        migrations.RemoveField(
            model_name='accounts',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='accounts',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='accounts',
            name='password',
        ),
        migrations.AddField(
            model_name='accounts',
            name='AccountID',
            field=models.CharField(default='0000000', max_length=30, unique=True, verbose_name='AccountID'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='Birthday',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Birthday'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='Contact_No',
            field=models.CharField(default='09212121212', max_length=30, verbose_name='Contact_No'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='Credit_Wallet',
            field=models.IntegerField(default=1, verbose_name='Credit'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='FirstName',
            field=models.CharField(default='Aaron', max_length=30, verbose_name='FirstName'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='LastName',
            field=models.CharField(default='Ayapana', max_length=30, verbose_name='LastName'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='Sec_Answer',
            field=models.CharField(default='Hello World!', max_length=30, verbose_name='Answer'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='Sec_Pin',
            field=models.CharField(default='0000', max_length=30, verbose_name='PIN'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='Sec_Question',
            field=models.TextField(default="What is a programmer's first words?", verbose_name='Question'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='Email',
            field=models.EmailField(default='default@gmail.com', max_length=50, unique=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='Password',
            field=models.CharField(default='Aaron123', max_length=30, verbose_name='Password'),
        ),
    ]
