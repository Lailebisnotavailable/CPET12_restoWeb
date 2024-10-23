# Generated by Django 5.1 on 2024-10-19 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GenkaiZoneRailImpact', '0004_alter_accounts_sec_pin'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodCatalog',
            fields=[
                ('FoodId', models.AutoField(primary_key=True, serialize=False)),
                ('FoodCategory', models.CharField(max_length=100)),
                ('FoodImage', models.ImageField(upload_to='food_images/')),
                ('FoodName', models.CharField(max_length=200)),
                ('FoodPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('FoodDescription', models.TextField()),
                ('FoodRating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('FoodViews', models.IntegerField(default=0)),
                ('DateAdded', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]