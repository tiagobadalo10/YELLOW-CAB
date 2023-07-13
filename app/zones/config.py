import os
import json
import base64
import re
import connexion
from google.cloud import bigquery
from google.oauth2.service_account import Credentials

def sanitize_label(label):
    sanitized_label = re.sub(r'[^a-zA-Z0-9_]', '_', label)
    return sanitized_label

connex_app = connexion.App(__name__, specification_dir=".")

app = connex_app.app

pod_name = sanitize_label(os.environ.get('POD_NAME'))
project_id = os.environ.get('PROJECT_ID')
dataset_name = os.environ.get('DATASET_NAME')
table_name = os.environ.get('TABLE_NAME')
encoded_key = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

service_account_key = base64.b64decode(encoded_key).decode("utf-8")
credentials = Credentials.from_service_account_info(
    json.loads(service_account_key))

client = bigquery.Client(project=project_id, credentials=credentials)
dataset_ref = client.dataset(dataset_name)
table_ref = dataset_ref.table(table_name)
