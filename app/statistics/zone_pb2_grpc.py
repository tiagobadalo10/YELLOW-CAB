# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import zone_pb2 as zone__pb2


class ZoneServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetZone = channel.unary_unary(
            '/zonepb.ZoneService/GetZone',
            request_serializer=zone__pb2.ZoneRequest.SerializeToString,
            response_deserializer=zone__pb2.ZoneResponse.FromString,
        )
        self.GetZones = channel.unary_unary(
            '/zonepb.ZoneService/GetZones',
            request_serializer=zone__pb2.ZonesRequest.SerializeToString,
            response_deserializer=zone__pb2.ZonesResponse.FromString,
        )


class ZoneServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetZone(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetZones(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ZoneServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'GetZone': grpc.unary_unary_rpc_method_handler(
            servicer.GetZone,
            request_deserializer=zone__pb2.ZoneRequest.FromString,
            response_serializer=zone__pb2.ZoneResponse.SerializeToString,
        ),
        'GetZones': grpc.unary_unary_rpc_method_handler(
            servicer.GetZones,
            request_deserializer=zone__pb2.ZonesRequest.FromString,
            response_serializer=zone__pb2.ZonesResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'zonepb.ZoneService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

 # This class is part of an EXPERIMENTAL API.


class ZoneService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetZone(request,
                target,
                options=(),
                channel_credentials=None,
                call_credentials=None,
                insecure=False,
                compression=None,
                wait_for_ready=None,
                timeout=None,
                metadata=None):
        return grpc.experimental.unary_unary(request, target, '/zonepb.ZoneService/GetZone',
                                             zone__pb2.ZoneRequest.SerializeToString,
                                             zone__pb2.ZoneResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetZones(request,
                 target,
                 options=(),
                 channel_credentials=None,
                 call_credentials=None,
                 insecure=False,
                 compression=None,
                 wait_for_ready=None,
                 timeout=None,
                 metadata=None):
        return grpc.experimental.unary_unary(request, target, '/zonepb.ZoneService/GetZones',
                                             zone__pb2.ZonesRequest.SerializeToString,
                                             zone__pb2.ZonesResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)