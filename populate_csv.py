import csv
from faker import Faker
import os

# Initialize Faker
fake = Faker()

# Define the input and output file names (update these paths as needed)
input_file = 'input.csv'  # Adjust the path if needed
output_file = 'output.csv'  # Adjust the path if needed

# Expected fieldnames based on your requirements
expected_fieldnames = ['Address', 'Price', 'first_name', 'last_name', 'phone', 'email', 'bedroom', 'squarefootage']

# Generate random bedroom count and square footage
def generate_bedroom_squarefootage():
    bedroom = fake.random_int(min=1, max=5)
    squarefootage = fake.random_int(min=500, max=4000)
    return bedroom, squarefootage

# Ensure the input file exists
if not os.path.exists(input_file):
    print(f"Input file {input_file} not found!")
    exit(1)

# Read the input CSV, populate missing data, and write to the output CSV
with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
    reader = csv.DictReader(infile)
    
    # Combine expected fieldnames with any additional fields in the input CSV
    fieldnames = reader.fieldnames
    for field in expected_fieldnames:
        if field not in fieldnames:
            fieldnames.append(field)
    
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in reader:
        if not row.get('first_name'):
            row['first_name'] = fake.first_name()
        if not row.get('last_name'):
            row['last_name'] = fake.last_name()
        if not row.get('phone'):
            row['phone'] = fake.phone_number()
        if not row.get('email'):
            row['email'] = fake.email()
        if not row.get('bedroom') or not row.get('squarefootage'):
            row['bedroom'], row['squarefootage'] = generate_bedroom_squarefootage()
        
        writer.writerow(row)

print(f"Data populated and saved to {output_file}")
