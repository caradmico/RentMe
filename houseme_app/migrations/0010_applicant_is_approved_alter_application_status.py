# Generated by Django 5.0.6 on 2024-06-09 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houseme_app', '0009_alter_applicant_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=50),
        ),
    ]
