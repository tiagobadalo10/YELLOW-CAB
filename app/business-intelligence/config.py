import pathlib
import os
import json
import base64
import re
import connexion
from google.cloud import bigquery, secretmanager
from google.oauth2.service_account import Credentials


def access_secret_version(secret_id, cre, version_id="latest"):

    secretClient = secretmanager.SecretManagerServiceClient(credentials=cre)

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = secretClient.access_secret_version(name=name)

    return response.payload.data.decode('UTF-8')

def sanitize_label(label):
    sanitized_label = re.sub(r'[^a-zA-Z0-9_]', '_', label)
    return sanitized_label

basedir = pathlib.Path(__file__).parent.resolve()

connex_app = connexion.FlaskApp(__name__, specification_dir=".")

app = connex_app.app

pod_name = sanitize_label(os.environ.get('POD_NAME'))

project_id = os.environ.get('PROJECT_ID')
dataset_name = os.environ.get('DATASET_NAME')
table_name = os.environ.get('TABLE_NAME')
encoded_key = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
zones_conn = os.environ.get("ZONES_CONNECTION")

service_account_key = base64.b64decode(encoded_key).decode("utf-8")
credentials = Credentials.from_service_account_info(
    json.loads(service_account_key))

auth0_domain = access_secret_version("auth0_domain", credentials)
auth0_audience = access_secret_version("auth0_audience", credentials)
auth0_issuer = access_secret_version("auth0_issuer", credentials)
auth0_algorithm = access_secret_version("auth0_algorithm", credentials)

client = bigquery.Client(project=project_id, credentials=credentials)

table_ref = client.dataset(dataset_name).table(table_name)
