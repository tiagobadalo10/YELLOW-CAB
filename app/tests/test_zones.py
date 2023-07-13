import json
import grpc
import zone_pb2
import zone_pb2_grpc
from google.protobuf.json_format import MessageToJson


IP = "127.0.0.1"
PORT = "50051"

def test_get_zone():
    with grpc.insecure_channel(f"{IP}:{PORT}") as channel:
        stub = zone_pb2_grpc.ZoneServiceStub(channel)
        response = stub.GetZone(zone_pb2.ZoneRequest(locationID=2))
        response_dict = json.loads(MessageToJson(response))
        expected_dict = {
            "zone": {"locationID": "2", "borough": "Queens", "serviceZone": "Jamaica Bay", "zone": "Boro Zone"}
        }
        assert response_dict == expected_dict


def test_get_zones():
    with grpc.insecure_channel(f"{IP}:{PORT}") as channel:
        stub = zone_pb2_grpc.ZoneServiceStub(channel)
        response = stub.GetZones(zone_pb2.ZonesRequest(
            zone=["Central Park", "Red Hook"]))
        response_dict = json.loads(MessageToJson(response))
        expected_dict = {
            'zones': [
                {'locationID': '43', 'borough': 'Manhattan',
                    'serviceZone': 'Central Park', 'zone': 'Yellow Zone'},
                {'locationID': '195', 'borough': 'Brooklyn',
                    'serviceZone': 'Red Hook', 'zone': 'Boro Zone'}
            ]
        }
        assert response_dict == expected_dict


test_get_zone()
test_get_zones()
