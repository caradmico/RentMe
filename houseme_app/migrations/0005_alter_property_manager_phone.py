# Generated by Django 3.2.25 on 2024-06-06 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houseme_app', '0004_auto_20240605_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='manager_phone',
            field=models.CharField(default='000-000-0000', max_length=20),
        ),
    ]