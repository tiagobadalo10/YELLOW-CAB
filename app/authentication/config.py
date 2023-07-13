import pathlib
import os
import base64
import json
import re
import connexion
from google.cloud import secretmanager
from google.oauth2.service_account import Credentials

def access_secret_version(secret_id, version_id="latest"):

    encoded_key = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    service_account_key = base64.b64decode(encoded_key).decode("utf-8")

    credentials = Credentials.from_service_account_info(
        json.loads(service_account_key))

    client = secretmanager.SecretManagerServiceClient(credentials=credentials)

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(name=name)

    return response.payload.data.decode('UTF-8')

def sanitize_label(label):
    sanitized_label = re.sub(r'[^a-zA-Z0-9_]', '_', label)
    return sanitized_label

basedir = pathlib.Path(__file__).parent.resolve()

connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

project_id = os.environ.get('PROJECT_ID')
pod_name = sanitize_label(os.environ.get('POD_NAME'))

app.secret_key = access_secret_version("app_secret_key")
auth0_client_id = access_secret_version("auth0_client_ID")
auth0_client_secret = access_secret_version("auth0_client_secret")
auth0_domain = access_secret_version("auth0_domain")
auth0_audience = access_secret_version("auth0_audience")
auth0_issuer = access_secret_version("auth0_issuer")
