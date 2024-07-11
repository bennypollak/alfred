import logging
import os
import boto3
from botocore.exceptions import ClientError
import json
from datetime import datetime
import requests

def to_dict(obj):
    if isinstance(obj, list):
        return [to_dict(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: to_dict(value) for key, value in obj.items()}
    elif hasattr(obj, "__dict__"):
        data = {}
        for attr in dir(obj):
            if not attr.startswith("__") and not callable(getattr(obj, attr)):
                value = getattr(obj, attr)
                data[attr] = to_dict(value)
        return data
    else:
        return obj

def get_ssml_response(text, voice='Matthew'):
    return f"<speak><voice name='{voice}'>{text}</voice></speak>"
def male_voice(text):
    return get_ssml_response(text, 'Matthew')
def female_voice(text):
    return get_ssml_response(text, 'Joanna')
def alfred_voice(text):
    return get_ssml_response(text, 'Matthew')

def slot_value(handler_input, name, default=None):
    intent_request = handler_input.request_envelope.request
    slots = intent_request.intent.slots
    value = default
    resolved_value = default
    # name = name.lower()
    print(f"Slot name: {name}")
    if name in slots:
        value = slots[name].value #.lower
        value = str(value).lower() if value else None
        resolved_value = value
        print(f"Slot {name} found as {value}")
        if value and slots[name].resolutions and slots[name].resolutions.resolutions_per_authority:
            resolution = slots[name].resolutions.resolutions_per_authority[0]
            if resolution.status.code.name == 'ER_SUCCESS_MATCH':
                resolved_value = resolution.values[0].value.name.lower()
                resolved_value = resolved_value.replace('.', '')
    print(f"Slot value: {value}, resolved value: {resolved_value}")
    return value, resolved_value

def send_request(url, payload={}, headers={}):
    try:
        print(f"Sending request to {url}")
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"Got result: {data}")
            return f'Success.'
        else:
            print("Failed to fetch data. Status code: {response.status_code}")
            return f'Failed.'
    except Exception as e:
        print(f"An error occurred: {e}")
        return f'Error.'

device_map = {
    "tv": {
        "small": {
            "device": "bedroom-tv",
            "short": "stv"
        },
        "big": {
            "device": "living-room-tv",
            "short": "btv"
        }
    },
    "tivo": {
        "small": {
            "device": "bedroom-tivo",
            "short": "st"
        },
        "big": {
            "device": "living-room-tivo",
            "short": "bt"
        }
    }
}
valid_rooms = ['small', 'big']
valid_devices = ['tv', 'tivo']
stations = {
    "cnn": 600, "abc": 507, "nbc": 502, "cbs": 502, "fox": 505, "espn": 570, "hbo": 899, "showtime": 865,
    "tiny": 4, "huge": 1000
}
def get_device(room, device='tv', short=False):
    if room not in valid_rooms or device not in valid_devices:
        return None
    return device_map[device][room]['short' if short else 'device']

def send_tv_request(room, commands='onoff'):
    device = get_device(room, 'tv')
    if not device:
        return f"TV not found in {room}"
    url = f"https://yo372002.ngrok.io/hubs/harmony-hub/devices/{device}/commands/{commands}"
    return send_request(url)

def send_channel_request(room, channel=None, station=None):
    device = get_device(room, 'tivo', short=True)
    if not device:
        return f"Tivo not found in {room}"
    slug = ''
    if station:
        channel = stations.get(station)
    if channel is None:
        return f"No station for {room}"
    for n in list(str(channel)):
        slug += f"{device}:{n},"
    slug = slug[:-1]
    url = f"https://yo372002.ngrok.io/hubs/harmony-hub/commandlist/{slug}"
    return send_request(url)




bucket_name = 'fd531fda-6127-49a9-b6dc-5d1754221ed0-us-east-1'
file_key = 'test.txt'
s3_client = boto3.client('s3')

def s3_read(bucket, key):
    """Read the content of an S3 file."""
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    return content

def s3_write(content, bucket=bucket_name, key=file_key, append=True, newline=True):
    if newline:
        content = '\n' + content
    if append:
        try:
            current_content = s3_read(bucket, key)
            content = current_content + content
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                pass
            else:
                raise
        s3_client.put_object(Bucket=bucket, Key=key, Body=content.encode('utf-8'))

echo_device_map = {
    "amzn1.ask.device.AMA6SNV7ZV7UGFBNWNIETNX7QQGECL34YVRGDCZWMDVJP5OORNHBIGCNLAHEBTRS625BU7J3GFUXWWGNVOT5RM3DEUVRTEWSPJFHIBK6LDBUPNRSOL427OWPOVZVIV2IPE4RZ7KLVBJ3DCDC55E3XRRLKKVQS5ZXCUZH6UTGPVPBGEU7AB2KILZM7BJB54C64BCETAMMIGBRJBSD": "livingroom",
    "amzn1.ask.device.AMAXBAW7JBUZYYPMO6WS4DQCGGCX7PWI63LRD626DQJMJXEDRHPM7FA3DUNXIQUHFSX57ZPXYCI5AFM7RHDHVIATSKHCURO4ETXQXNHTYNV4WSQV4DB2TZWCIPSCF6UF2JGNJRQF2L5W4AYRBJD2MO6P4TH2VLN4SK67D2EFYGO4TX3BKUNXGIHXKTDZIS62ROMBW": "retired",
    "amzn1.ask.device.AMATH75Q4RFEKCXKEU4GLKJEGJ2BEDAVFUWKMIU3LHHVUVGK2NBKJUOO447U55GIUJMLOMJPS7ED6FSQ2GTYQE4LI5CO3PHCYSNTVCGI4ORL5YN2MFY76SSTVL22TYQORFDC2445S3SHZEQAMAO556QQLSCRHZXF3OJJ4DVAQHCXMAQRQSGY2BIIUMVEEVOKLM4CNGV7RD77Z2KP": "bedroom",
    "amzn1.ask.device.AMAXJAPA4OTSER5H6YZ2LVKHQAKL4FTPBEWPSFMKEDCT5Z7UF3EYUREQ7O7F2SHLZJPYFRY3HY4E2DAFNUZYRUD6PUSGNN7ZWAH4MPOJL2UGRFSGEHVTSKVLHFISTGH3UFYSVAIOGHG4ONSE6IIJVYWAUWZRQW2SOWTRHLOTBEVTWSFRRNQA646J7VHEH3D2GDHI22DYP2YX6KI": "kitchen",
    "amzn1.ask.device.AMA5R44WCBSXEWTJ4ILRVBZNPLXHB24I5FTG5E6EQ5P5KB2GDX3IISOHCN6TNXLCSNPNWITESBC4J7DGJDIEN62D2XOVG3U4XRVGP4P6M2YFUEFNDLLGHPMULKO43KM7J5H75ZEB5GPJ77TVQUF7VRGRPRUSBUYXVJ2BP6TY5XTYENYJY733MLJ3NHTDAUD7SKZDWJD6NPJL3CQ": "test",
    "amzn1.ask.device.AMA4UBAJ5A3XUSANPNJWCEHQIYC5FWEARFWN3VKIKUQIV7Q72FXGYLCOXAS56FRTSP2FBYLJKBBYTOLZRX35YKQNJ6QEU7QFWDIXATZTYECP2VYOGV46OHHW35GEOGKOIUS536EVP4NOZ55R5JW7CKKAO4IEZNCXAV3YVT6ARRESWAGAQTRXG65VXYWJGYITC2ABLGONYSMCDLYH": "iphone",
    "amzn1.ask.device.AMAZ5FPGYM43LH3SO7RAQX7UEJFN4Y5IWUVHSMZDNEKHBKUXYG3VOTJAHFHSH3ENLDNHZQINHBCTVYFBLCRWRZKKWASCBORGOILNEMF5WMZ4NTUBF5FW4FK7SFLVJ6G2GQ3TKHXUEPHKI7NYCZXZUY6L3DIZQ6UFJRUSNQVRITLLHSN2YH3QDZ36DM2UJ32NVPPQJH2ANYSFY363": "desk"
}
def echo_device_name(handler_input):
    device_id = handler_input.request_envelope.context.system.device.device_id
    return echo_device_map.get(device_id, "unknown")
