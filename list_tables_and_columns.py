import os
import django
from django.apps import apps

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'houseme_project.settings')
django.setup()

# Function to get tables and columns
def list_tables_and_columns():
    for model in apps.get_models():
        print(f'Table: {model._meta.db_table}')
        for field in model._meta.fields:
            print(f'  Column: {field.name} - {field.get_internal_type()}')

# Call the function
list_tables_and_columns()
