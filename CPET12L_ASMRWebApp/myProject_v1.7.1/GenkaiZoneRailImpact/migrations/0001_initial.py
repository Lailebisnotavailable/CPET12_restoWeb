# Generated by Django 5.1.1 on 2025-01-10 23:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('AccountID', models.AutoField(primary_key=True, serialize=False)),
                ('AccountType', models.CharField(max_length=30, null=True, verbose_name='Account Type')),
                ('FirstName', models.CharField(max_length=30, verbose_name='First Name')),
                ('LastName', models.CharField(max_length=30, verbose_name='Last Name')),
                ('Password', models.CharField(default='P@ssw0rd', max_length=255, verbose_name='Password')),
                ('Email', models.EmailField(max_length=50, unique=True, verbose_name='Email')),
                ('Birthday', models.DateField(blank=True, null=True)),
                ('ContactNo', models.CharField(max_length=11, null=True, unique=True, verbose_name='Contact No.')),
                ('Wallet', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True, verbose_name='Wallet')),
                ('BlockLot', models.CharField(max_length=100, null=True, verbose_name='Block & Lot')),
                ('Street', models.CharField(max_length=100, null=True, verbose_name='Street')),
                ('Subdivision', models.CharField(max_length=100, null=True, verbose_name='Subdivision')),
                ('Barangay', models.CharField(max_length=100, null=True, verbose_name='Barangay')),
                ('City', models.CharField(max_length=100, null=True, verbose_name='City')),
                ('Province', models.CharField(max_length=100, null=True, verbose_name='Province')),
            ],
        ),
        migrations.CreateModel(
            name='CashierApplication',
            fields=[
                ('ApplicantID', models.AutoField(primary_key=True, serialize=False)),
                ('AccountType', models.CharField(max_length=30, null=True, verbose_name='Account Type')),
                ('FirstName', models.CharField(max_length=30, verbose_name='First Name')),
                ('LastName', models.CharField(max_length=30, verbose_name='Last Name')),
                ('Password', models.CharField(default='P@ssw0rd', max_length=255, verbose_name='Password')),
                ('Email', models.EmailField(max_length=50, unique=True, verbose_name='Email')),
                ('Birthday', models.DateField(blank=True, null=True)),
                ('ContactNo', models.CharField(max_length=11, null=True, unique=True, verbose_name='Contact No.')),
                ('Sec_Question', models.CharField(max_length=200, null=True, verbose_name='Security Question')),
                ('Sec_Answer', models.CharField(blank=True, max_length=50, null=True, verbose_name='Security Answer')),
                ('Sec_Pin', models.CharField(max_length=4, null=True, verbose_name='Security PIN')),
                ('last_login', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FoodCatalog',
            fields=[
                ('FoodId', models.AutoField(primary_key=True, serialize=False)),
                ('FoodCategory', models.CharField(blank=True, max_length=30, null=True, verbose_name='Category')),
                ('FoodImage', models.ImageField(blank=True, null=True, upload_to='food_images/')),
                ('FoodName', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('FoodPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('FoodDescription', models.TextField(blank=True, null=True)),
                ('FoodViews', models.IntegerField(blank=True, default=0, null=True)),
                ('DateAdded', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('CheckoutID', models.AutoField(primary_key=True, serialize=False)),
                ('OrderID', models.IntegerField(default=0)),
                ('Quantity', models.IntegerField(default=1)),
                ('Status', models.CharField(default='Standby', max_length=100, null=True, verbose_name='Status')),
                ('AccountID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GenkaiZoneRailImpact.accounts')),
                ('FoodID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GenkaiZoneRailImpact.foodcatalog')),
            ],
        ),
        migrations.CreateModel(
            name='TopUp',
            fields=[
                ('TopUpID', models.AutoField(primary_key=True, serialize=False)),
                ('Status', models.CharField(default='pending', max_length=10)),
                ('TopUpAmount', models.IntegerField(default=1)),
                ('TransactionDate', models.DateTimeField(auto_now_add=True, null=True)),
                ('AccountID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GenkaiZoneRailImpact.accounts')),
            ],
        ),
        migrations.CreateModel(
            name='Void',
            fields=[
                ('VoidID', models.AutoField(primary_key=True, serialize=False)),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('Checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GenkaiZoneRailImpact.checkout')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('CartID', models.AutoField(primary_key=True, serialize=False)),
                ('Quantity', models.IntegerField(default=1)),
                ('AccountID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GenkaiZoneRailImpact.accounts')),
                ('FoodID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GenkaiZoneRailImpact.foodcatalog')),
            ],
            options={
                'unique_together': {('AccountID', 'FoodID')},
            },
        ),
    ]
