# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zone.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nzone.proto\x12\x06zonepb\"!\n\x0bZoneRequest\x12\x12\n\nlocationID\x18\x01 \x01(\x03\"\x1c\n\x0cZonesRequest\x12\x0c\n\x04zone\x18\x01 \x03(\t\",\n\rZonesResponse\x12\x1b\n\x05zones\x18\x01 \x03(\x0b\x32\x0c.zonepb.Zone\"*\n\x0cZoneResponse\x12\x1a\n\x04zone\x18\x01 \x01(\x0b\x32\x0c.zonepb.Zone\"O\n\x04Zone\x12\x12\n\nlocationID\x18\x01 \x01(\x03\x12\x0f\n\x07\x62orough\x18\x02 \x01(\t\x12\x14\n\x0cservice_zone\x18\x03 \x01(\t\x12\x0c\n\x04zone\x18\x04 \x01(\t2\x80\x01\n\x0bZoneService\x12\x36\n\x07GetZone\x12\x13.zonepb.ZoneRequest\x1a\x14.zonepb.ZoneResponse\"\x00\x12\x39\n\x08GetZones\x12\x14.zonepb.ZonesRequest\x1a\x15.zonepb.ZonesResponse\"\x00\x62\x06proto3')


_ZONEREQUEST = DESCRIPTOR.message_types_by_name['ZoneRequest']
_ZONESREQUEST = DESCRIPTOR.message_types_by_name['ZonesRequest']
_ZONESRESPONSE = DESCRIPTOR.message_types_by_name['ZonesResponse']
_ZONERESPONSE = DESCRIPTOR.message_types_by_name['ZoneResponse']
_ZONE = DESCRIPTOR.message_types_by_name['Zone']
ZoneRequest = _reflection.GeneratedProtocolMessageType('ZoneRequest', (_message.Message,), {
    'DESCRIPTOR': _ZONEREQUEST,
    '__module__': 'zone_pb2'
    # @@protoc_insertion_point(class_scope:zonepb.ZoneRequest)
})
_sym_db.RegisterMessage(ZoneRequest)

ZonesRequest = _reflection.GeneratedProtocolMessageType('ZonesRequest', (_message.Message,), {
    'DESCRIPTOR': _ZONESREQUEST,
    '__module__': 'zone_pb2'
    # @@protoc_insertion_point(class_scope:zonepb.ZonesRequest)
})
_sym_db.RegisterMessage(ZonesRequest)

ZonesResponse = _reflection.GeneratedProtocolMessageType('ZonesResponse', (_message.Message,), {
    'DESCRIPTOR': _ZONESRESPONSE,
    '__module__': 'zone_pb2'
    # @@protoc_insertion_point(class_scope:zonepb.ZonesResponse)
})
_sym_db.RegisterMessage(ZonesResponse)

ZoneResponse = _reflection.GeneratedProtocolMessageType('ZoneResponse', (_message.Message,), {
    'DESCRIPTOR': _ZONERESPONSE,
    '__module__': 'zone_pb2'
    # @@protoc_insertion_point(class_scope:zonepb.ZoneResponse)
})
_sym_db.RegisterMessage(ZoneResponse)

Zone = _reflection.GeneratedProtocolMessageType('Zone', (_message.Message,), {
    'DESCRIPTOR': _ZONE,
    '__module__': 'zone_pb2'
    # @@protoc_insertion_point(class_scope:zonepb.Zone)
})
_sym_db.RegisterMessage(Zone)

_ZONESERVICE = DESCRIPTOR.services_by_name['ZoneService']
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _ZONEREQUEST._serialized_start = 22
    _ZONEREQUEST._serialized_end = 55
    _ZONESREQUEST._serialized_start = 57
    _ZONESREQUEST._serialized_end = 85
    _ZONESRESPONSE._serialized_start = 87
    _ZONESRESPONSE._serialized_end = 131
    _ZONERESPONSE._serialized_start = 133
    _ZONERESPONSE._serialized_end = 175
    _ZONE._serialized_start = 177
    _ZONE._serialized_end = 256
    _ZONESERVICE._serialized_start = 259
    _ZONESERVICE._serialized_end = 387
# @@protoc_insertion_point(module_scope)
