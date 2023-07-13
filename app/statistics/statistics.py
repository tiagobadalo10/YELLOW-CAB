import grpc
import zone_pb2
import zone_pb2_grpc
from flask import jsonify, make_response
from config import table_ref, client, zones_conn, pod_name
from prometheus_client import Summary, Counter
from utils import VerifyToken

# METRICS
REQUEST_TIME = Summary('request_processing_seconds_statistics',
                       'Time spent processing a request', labelnames=['pod'])
REQUEST_COUNT = Counter('requests_total_statistics',
                        'Total number of requests received', labelnames=['pod'])
REQUEST_FAILURE_COUNT = Counter(
    'requests_failure_total_statistics', 'Total number of failures', labelnames=['pod'])

# HEALTH CHECK
def health():
    return 200

# TIME
@REQUEST_TIME.labels(pod_name).time()
def get_time_stats(PULocationName, DOLocationName, PULocationName2, DOLocationName2, token):

    REQUEST_COUNT.labels(pod_name).inc()

    if not is_valid_access_token(token):
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return make_text_plain_response('Unauthorized. Access token is not valid', 401)

    zones_array1 = list(get_zone_details([PULocationName, DOLocationName]).zones)
    zones_array2 = list(get_zone_details([PULocationName2, DOLocationName2]).zones)

    if invalidNames(zones_array1) or invalidNames(zones_array2):
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return make_text_plain_response('Invalid Names supplied', 400)

    PULocationID1 = zones_array1[0].locationID
    DOLocationID1 = zones_array1[1].locationID
    PULocationID2 = zones_array2[0].locationID
    DOLocationID2 = zones_array2[1].locationID

    query1 = f"SELECT ROUND(MIN(duration_minutes), 2), ROUND(MAX(duration_minutes), 2), \
    ROUND(AVG(duration_minutes), 2) FROM {table_ref} WHERE PULocationID = {PULocationID1} \
    AND DOLocationID = {DOLocationID1}"
    result1 = do_query(query1)
    query2 = f"SELECT ROUND(MIN(duration_minutes), 2), ROUND(MAX(duration_minutes), 2), \
    ROUND(AVG(duration_minutes), 2) FROM {table_ref} WHERE PULocationID = {PULocationID2} \
    AND DOLocationID = {DOLocationID2}"
    result2 = do_query(query2)

    if not result1 or not result2:
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return "Not Found: Route time statistics not found", 404

    return jsonify({
        "trip1": {
            "min_time": result1[0]["f0_"],
            "max_time": result1[0]["f1_"],
            "avg_time": result1[0]["f2_"],
        },
        "trip2": {
            "min_time": result2[0]["f0_"],
            "max_time": result2[0]["f1_"],
            "avg_time": result2[0]["f2_"],
        }})

# CONGESTION
@REQUEST_TIME.labels(pod_name).time()
def get_congestion_stats(PULocationName, DOLocationName, PULocationName2, DOLocationName2, token):

    REQUEST_COUNT.labels(pod_name).inc()

    if not is_valid_access_token(token):
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return make_text_plain_response('Unauthorized. Access token is not valid', 401)

    zones_array1 = list(get_zone_details([PULocationName, DOLocationName]).zones)
    zones_array2 = list(get_zone_details([PULocationName2, DOLocationName2]).zones)

    if invalidNames(zones_array1) or invalidNames(zones_array2):
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return make_text_plain_response('Invalid Names supplied', 400)

    PULocationID1 = zones_array1[0].locationID
    DOLocationID1 = zones_array1[1].locationID
    PULocationID2 = zones_array2[0].locationID
    DOLocationID2 = zones_array2[1].locationID

    query1 = f"SELECT ROUND(MIN(congestion_surcharge), 2), ROUND(MAX(congestion_surcharge), 2), \
    ROUND(AVG(congestion_surcharge), 2) FROM {table_ref} WHERE PULocationID = {PULocationID1} \
    AND DOLocationID = {DOLocationID1}"
    result1 = do_query(query1)
    query2 = f"SELECT ROUND(MIN(congestion_surcharge), 2), ROUND(MAX(congestion_surcharge), 2), \
    ROUND(AVG(congestion_surcharge), 2) FROM {table_ref} WHERE PULocationID = {PULocationID2} \
    AND DOLocationID = {DOLocationID2}"
    result2 = do_query(query2)

    if not result1 or not result2:
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return "Not Found: Route time statistics not found", 404

    return jsonify({
        "trip1": {
            "min_congestion": result1[0]["f0_"],
            "max_congestion": result1[0]["f1_"],
            "avg_congestion": result1[0]["f2_"],
        },
        "trip2": {
            "min_congestion": result2[0]["f0_"],
            "max_congestion": result2[0]["f1_"],
            "avg_congestion": result2[0]["f2_"],
        }})


# CAB
@REQUEST_TIME.labels(pod_name).time()
def get_cab_stats(LocationName, LocationName2, token):

    REQUEST_COUNT.labels(pod_name).inc()

    if not is_valid_access_token(token):
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return make_text_plain_response('Unauthorized. Access token is not valid.', 401)

    zones_details = get_zone_details([LocationName, LocationName2])
    zones_array = list(zones_details.zones)

    locationID1 = zones_array[0].locationID
    locationID2 = zones_array[1].locationID

    if not locationID1 or not locationID2:
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return "Bad Request: Missing required parameter 'locationName'", 400

    locationID1 = int(locationID1)
    locationID2 = int(locationID2)

    query1 = f"SELECT COUNT(*) FROM zone_locations.stats_table WHERE PULocationID = {locationID1} \
    OR DOLocationID = {locationID1}"
    result1 = do_query(query1)
    query2 = f"SELECT COUNT(*) FROM zone_locations.stats_table WHERE PULocationID = {locationID2} \
    OR DOLocationID = {locationID2}"
    result2 = do_query(query2)

    if not result1 or not result2:
        REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return "Not Found: Route time statistics not found", 404

    return jsonify({"number_cabs_first_location": result1[0]["f0_"],
                    "number_cabs_second_location": result2[0]["f0_"]})

def invalidNames(zones_array):
    return len(zones_array) != 2


def make_text_plain_response(text, code):
    response = make_response(text, code)
    response.headers['Content-Type'] = 'text/plain'
    return response


def do_query(query):
    query_job = client.query(query)
    results = query_job.to_dataframe().to_dict(orient='records')
    return results


def get_zone_details(zones_names):
    with grpc.insecure_channel(zones_conn) as channel:
        stub = zone_pb2_grpc.ZoneServiceStub(channel)
        response = stub.GetZones(zone_pb2.ZonesRequest(zone=zones_names))
        return response


def is_valid_access_token(access_token):
    verifier = VerifyToken(access_token)
    payload = verifier.verify()
    if payload.get("status"):
        return False
    return True
