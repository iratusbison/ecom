# Generated by Django 4.0.6 on 2024-07-26 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_order_address_alter_order_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='reward_points',
            field=models.IntegerField(default=0),
        ),
    ]
