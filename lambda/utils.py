import logging
import json
from datetime import datetime
import requests
from configs import echo_device_map, room_map, valid_devices, station_to_channel_map, \
    device_names_map, commands_map

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
        value = str(value).lower() if value else default
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

def room_echo_device_in(handler_input):
    device_name = echo_device_name(handler_input)
    return room_map.get(device_name)

def process_request(session_attributes):
    intent_name = session_attributes.get('intent_name')
    room = session_attributes.get('intended_room_name')
    action = session_attributes.get('action')
    if not action:
        return f"No action defined for {intent_name}"
    command_info = commands_map.get(action)
    device = command_info['device']
    device = device_names_map[device][room]
    commands = []
    if intent_name == 'ScreenActionIntent':
        command = command_info['command']
        print(f"Action: {action}, Command: {command}")
        if command and isinstance(command, dict):
            command = command.get(room)
            print(f"Command: {command}")
        if not command:
            return f"No command found for {action} in {room}"
        commands = [command]
    elif intent_name == 'ChannelIntent':
        channel = session_attributes.get('channel_number')
        station = session_attributes.get('intended_station')
        if station:
            channel = station_to_channel_map.get(station)
        if channel is None:
            return f"No station for {room}"
        commands = list(str(channel))
    else:
        command = command_info.get('command')
        commands = [command]

    slug = ''
    for command in commands:
        slug += f"{device}:{command},"
    slug = slug[:-1]
    url = f"https://yo372002.ngrok.io/hubs/harmony-hub/commandlist/{slug}"
    return send_request(url)

def echo_device_name(handler_input):
    device_id = handler_input.request_envelope.context.system.device.device_id
    return echo_device_map.get(device_id, "unknown")

def dump_request(handler_input):
    intent_request = handler_input.request_envelope.request
    session_attributes = handler_input.attributes_manager.session_attributes
    print("Intent Request Object: " + json.dumps(to_dict(intent_request)))
    print("Session Attributes: " + json.dumps(session_attributes))

def camel_to_space(input_string):
    result = ""
    for char in input_string:
        if char.isupper():
            result += " " + char.lower()
        else:
            result += char
    return result.lstrip()

