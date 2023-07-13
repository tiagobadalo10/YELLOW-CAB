import json
from urllib.parse import quote_plus, urlencode
import base64
from config import app, auth0_domain, auth0_client_id, auth0_client_secret, auth0_audience, auth0_issuer, pod_name
from flask import render_template, session, redirect, url_for, request
from prometheus_client import Summary, Counter
import requests

# METRICS
REQUEST_TIME = Summary(
    'request_processing_seconds_authentication', 'Time spent processing a request', labelnames=['pod'])
REQUEST_COUNT = Counter('requests_total_authentication',
                        'Total number of requests received', labelnames=['pod'])

# HEALTH CHECK
def health():
    return 200

# HOME
@REQUEST_TIME.labels(pod_name).time()
def home():

    REQUEST_COUNT.labels(pod_name).inc()

    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=3)
    )


@app.route("/api/authentication/callback", methods=["GET", "POST"])
def callback():
    code = request.args.get('code')
    url = f"{auth0_issuer}oauth/token"
    data = {
        "grant_type" : "authorization_code",
        "client_id" : auth0_client_id,
        "client_secret" : auth0_client_secret,
        "code" : code,
        "redirect_uri" : url_for("callback", _external=True),
    }

    response = requests.post(url, data=data, timeout=10)
    json_response = json.loads(response.text)
    id_token = json_response["id_token"]
    id_token_payload = base64_to_string(extract_payload(id_token))
    id_token_json = json.loads(id_token_payload)
    json_response.update(id_token_json)
    session["user"] = json_response

    return redirect("/api/authentication")

# LOGIN
@REQUEST_TIME.labels(pod_name).time()
def login():

    REQUEST_COUNT.labels(pod_name).inc()

    authorize_endpoint = "authorize"
    response_type = "code"
    redirect_uri = url_for("callback", _external=True)
    scope = "openid profile email"

    # Construir os parâmetros da URL de redirecionamento
    params = {
        "response_type": response_type,
        "client_id": auth0_client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "audience": auth0_audience
    }

    # Codificar os parâmetros na URL
    encoded_params = urlencode(params)

    # Construir a URL de redirecionamento completa
    redirect_url = f"{auth0_issuer}{authorize_endpoint}?{encoded_params}"

    return redirect(redirect_url)


# LOGOUT
@REQUEST_TIME.labels(pod_name).time()
def logout():

    REQUEST_COUNT.labels(pod_name).inc()

    session.clear()
    return redirect(
        "https://"
        + auth0_domain
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for('/api.authentication_home', _external=True),
                "client_id": auth0_client_id,
            },
            quote_via=quote_plus,
        )
    )


def extract_payload(token):
    parts = token.split(".")
    if len(parts) == 3:
        return parts[1]
    return None

def base64_to_string(base64_str):
    # Remover caracteres não permitidos e adicionar padding se necessário
    base64_str = base64_str.replace("-", "+").replace("_", "/")
    padding = len(base64_str) % 4
    if padding:
        base64_str += "=" * (4 - padding)

    # Decodificar a string em Base64
    decoded_bytes = base64.b64decode(base64_str)
    decoded_str = decoded_bytes.decode("utf-8")

    return decoded_str
