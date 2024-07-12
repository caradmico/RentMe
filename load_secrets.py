import hvac
import os

def load_secrets():
    # Initialize the Vault client
    client = hvac.Client(
        url=os.getenv('VAULT_ADDR'),
        token=os.getenv('VAULT_TOKEN'),
    )

    # Read the secrets from Vault
    secret_path = 'path/to/your/secrets'
    secrets = client.secrets.kv.v2.read_secret_version(path=secret_path)['data']['data']

    # Set environment variables
    os.environ['SECRET_KEY'] = secrets['SECRET_KEY']
    os.environ['DB_NAME'] = secrets['DB_NAME']
    os.environ['DB_USER'] = secrets['DB_USER']
    os.environ['DB_PASSWORD'] = secrets['DB_PASSWORD']
    os.environ['DB_HOST'] = secrets['DB_HOST']
    os.environ['DB_PORT'] = str(secrets['DB_PORT'])

# Load secrets
load_secrets()
