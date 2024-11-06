# Generated by Django 5.1.3 on 2024-11-06 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Category name must be unique', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='name',
            field=models.CharField(help_text='Manufacturer name must be unique', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(help_text='Product name must be unique', max_length=200, unique=True),
        ),
    ]