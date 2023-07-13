import grpc
import zone_pb2
import zone_pb2_grpc
from flask import jsonify, make_response
from config import table_ref, client, zones_conn, pod_name
from prometheus_client import Summary, Counter
from utils import VerifyToken

# METRICS
REQUEST_TIME = Summary(
    'request_processing_seconds_business_intelligence', 'Time spent processing a request', labelnames=['pod'])
REQUEST_COUNT = Counter('requests_total_business_intelligence',
                        'Total number of requests received', labelnames=['pod'])
REQUEST_FAILURE_COUNT = Counter(
    'requests_failure_total_business_intelligence', 'Total number of failures', labelnames=['pod'])

# HEALTH CHECK
def health():
    return 200

# TIP
@REQUEST_TIME.labels(pod_name).time()
def get_tip_stats(PULocationName, DOLocationName, token):

    REQUEST_COUNT.labels(pod_name).inc()

    if not is_authorized(token):
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return make_text_plain_response('Unauthorized. Access token is not valid.', 401)

    zones_details = get_zone_details([PULocationName, DOLocationName])
    zones_array = list(zones_details.zones)

    if invalidId(zones_array):
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return make_text_plain_response('Invalid ID supplied', 400)

    PULocationID = zones_array[0].locationID
    DOLocationID = zones_array[1].locationID

    query = f"SELECT * FROM `{table_ref}` WHERE PULocationID = {PULocationID} AND DOLocationID = {DOLocationID}"
    cab_rides = do_query(query)

    if len(cab_rides) == 0:
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return make_text_plain_response('Tips statistics not found', 404)

    tip_amounts = [ride.get('tip_amount') for ride in cab_rides]

    size_tips_amounts = len(tip_amounts)

    return jsonify({
        'count_tips': size_tips_amounts,
        'max_tips': round(max(tip_amounts), 2),
        'min_tips': round(min(tip_amounts), 2),
        'avg_tips': round(sum(tip_amounts) / size_tips_amounts, 2),
    })

# AMOUNT
@REQUEST_TIME.labels(pod_name).time()
def get_amount_stats(PULocationName, DOLocationName, token):

    REQUEST_COUNT.labels(pod_name).inc()

    if not is_authorized(token):
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return make_text_plain_response('Unauthorized. Access token is not valid.', 401)

    zones_details = get_zone_details([PULocationName, DOLocationName])
    zones_array = list(zones_details.zones)

    if invalidId(zones_array):
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return make_text_plain_response('Invalid ID supplied', 400)

    PULocationID = zones_array[0].locationID
    DOLocationID = zones_array[1].locationID

    query = f"SELECT * FROM `{table_ref}` WHERE PULocationID = {PULocationID} AND DOLocationID = {DOLocationID}"
    cab_rides = do_query(query)

    if len(cab_rides) == 0:
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return make_text_plain_response('Amount statistics not found', 404)

    amounts = [ride.get('total_amount') for ride in cab_rides]

    return jsonify({
        "count_amount": len(amounts),
        "total_amount": round(sum(amounts), 2),
        "min_amount": round(min(amounts), 2),
        "max_amount": round(max(amounts), 2),
        "avg_amount": round(sum(amounts) / len(amounts), 2),
    })


def invalidId(zones_array):
    return len(zones_array) != 2


def make_text_plain_response(text, code):
    response = make_response(text, code)
    response.headers['Content-Type'] = 'text/plain'
    return response


def get_zone_details(zones_names):
    with grpc.insecure_channel(zones_conn) as channel:
        stub = zone_pb2_grpc.ZoneServiceStub(channel)
        response = stub.GetZones(zone_pb2.ZonesRequest(zone=zones_names))
        return response


def do_query(query):
    query_job = client.query(query)
    results = query_job.to_dataframe().to_dict(orient='records')
    return results


def is_authorized(access_token):
    verifier = VerifyToken(access_token, permissions=['read:admin'])
    payload = verifier.verify()
    if payload.get("status"):
        return False
    return True
