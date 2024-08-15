# Generated by Django 4.0.6 on 2024-08-15 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0038_delete_adimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='store.customer')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.address'),
        ),
    ]
