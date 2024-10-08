# Generated by Django 4.0.6 on 2024-08-15 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0039_remove_order_phone_address_alter_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='attribute_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.attributekey'),
        ),
        migrations.AddField(
            model_name='order',
            name='attribute_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.attributevalue'),
        ),
    ]
