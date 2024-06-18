# houseme_app/migrations/0004_auto_20240605_1626.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('houseme_app', '0003_profile'),  # Update this line with the correct dependency
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='pets_allowed',
            field=models.CharField(max_length=50, default='No'),
        ),
        migrations.AlterField(
            model_name='property',
            name='lease_terms',
            field=models.CharField(max_length=50, default='Month-to-Month'),
        ),
        # Add any other fields that need length updates here
    ]
