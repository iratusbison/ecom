# Generated by Django 4.0.6 on 2024-08-11 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_alter_productattributemapping_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productattributemapping',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='productattributemapping',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='productattributemapping',
            name='product',
        ),
        migrations.DeleteModel(
            name='ProductAttribute',
        ),
        migrations.DeleteModel(
            name='ProductAttributeKey',
        ),
        migrations.DeleteModel(
            name='ProductAttributeMapping',
        ),
    ]
