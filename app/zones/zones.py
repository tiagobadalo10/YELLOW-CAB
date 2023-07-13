from prometheus_client import Summary, Counter
import zone_pb2
import zone_pb2_grpc
from config import table_ref, client, pod_name

# METRICS
REQUEST_TIME = Summary('request_processing_seconds_zones',
                       'Time spent processing a request', labelnames=['pod'])
REQUEST_COUNT = Counter('requests_total_zones',
                        'Total number of requests received', labelnames=['pod'])
REQUEST_FAILURE_COUNT = Counter(
    'requests_failure_total_zones', 'Total number of failures', labelnames=['pod'])


class ZoneService(zone_pb2_grpc.ZoneServiceServicer):

    @REQUEST_TIME.labels(pod_name).time()
    def GetZone(self, request, context):

        REQUEST_COUNT.labels(pod_name).inc()

        locationID = request.locationID

        query = f"SELECT * FROM {table_ref} WHERE LocationID IN ({locationID})"

        query_job = client.query(query)

        result = query_job.result()

        if result is not None:

            for row in result:

                v1, v2, v3, v4 = row

                response = zone_pb2.ZoneResponse(zone=zone_pb2.Zone(
                    locationID=v1, borough=v2, service_zone=v3, zone=v4))

        else:
            REQUEST_FAILURE_COUNT.labels(pod_name).inc()
        return response

    @REQUEST_TIME.labels(pod_name).time()
    def GetZones(self, request, context):

        REQUEST_COUNT.labels(pod_name).inc()

        zone_names = request.zone
        response = []

        for name in zone_names:

            query = f"SELECT * FROM {table_ref} WHERE Zone IN ('{name}')"

            query_job = client.query(query)

            result = query_job.result()

            if result is not None:

                for row in result:

                    v1, v2, v3, v4 = row

                    response.append(zone_pb2.Zone(
                        locationID=v1, borough=v2, service_zone=v3, zone=v4))

            else:
                REQUEST_FAILURE_COUNT.labels(pod_name).inc()

        return zone_pb2.ZonesResponse(zones=response)

    def HealthCheck(self, request, context):
        return zone_pb2.HealthCheckResponse(status="200")
