import logging
import json
from datetime import datetime
import requests
from configs import echo_device_map, room_map, valid_devices, station_to_channel_map, \
    device_names_map, commands_map, device_types

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

def get_query_utterance(handler_input):
    slots = handler_input.request_envelope.request.intent.slots
    query = slots['query'].value if 'query' in slots and slots['query'].value else None
    return query

def slot_value(handler_input, name, default=None):
    intent_request = handler_input.request_envelope.request
    slots = intent_request.intent.slots
    value = default
    resolved_value = default
    # name = name.lower()
    print(f"Slot name: {name}")
    if slots and name in slots:
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
            #
            data = response.text
            print(f"Got result: {data}")
            return f'Ok'
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
    path = ''
    url = None
    if intent_name == 'DeviceIntent':
        intended_on_off = session_attributes.get('intended_on_off')
        intended_device = session_attributes.get('intended_device')
        device_type = device_types.get(intended_device, 'unknown')['type']
        intended_device = intended_device.lower().replace(' ', '%20')
        print(f"Device: {intended_device} On/Off: {intended_on_off}")
        path = f"devices/{device_type}:{intended_device}:{intended_on_off}"
    elif intent_name == 'AirIntent':
        on_off = session_attributes.get('on_off')
        temp = session_attributes.get('temp')
        room_number = 'one' if room == 'small' else 'two'
        print(f"Room: {room}, Room Number: {room_number} Temp: {temp} On/Off: {on_off}")
        if temp:
            if temp == 'current':
                path = f"wemo/thermo/set/{room_number}"
            else:
                value = 0.4 if temp == 'hotter' else -0.3
                path = f"wemo/thermo/{room_number}/{value}"
        else:
            path = f"wemo/thermo/{room_number}" if on_off == 'on' else f"wemo/cycle/{room_number}/0"
    else:
        times = int(session_attributes.get('intended_times', 1))
        action = session_attributes.get('intended_action')
        if not action:
            return f"No action defined for {intent_name}"
        commands = commands_map.get(action)
        if intent_name == 'ChannelIntent':
            channel = session_attributes.get('channel_number')
            station = session_attributes.get('intended_station')
            if station:
                channel = station_to_channel_map.get(station)
            if channel is None:
                return {
                    "response": f"No station for {room}",
                    "url": ''
                }
            commands = []
            for channel in list(str(channel)):
                commands.append( { "device": "tivo", "command": channel, "count": 1 } )
        else:
            if not isinstance(commands, list) and commands['device'] == 'url':
                url = commands.get('command').get(room)
            else:
                if not isinstance(commands, list):
                    commands = [ commands ]
                print(f"Commands: {commands}")
                for i in range(len(commands)):
                    command = commands[i]
                    if not 'command' in command:
                        command['command'] = action
                    command_action = command.get('command')
                    if command_action and isinstance(command_action, dict):
                        print(f"Command_action0: {command_action}")
                        command = command.copy()
                        command['command'] = command_action.get(room)
                        commands[i] = command
                        print(f"Command: {commands[i]}")
                # if not command:
                #     return f"No command found for {action} in {room}"
        if not url:
            slug = ''
            for _ in range(times):
                for command in commands:
                    count = command.get('count', 1)
                    for _ in range(count):
                        device = device_names_map[command['device']][room]
                        print(f"Command: {command}, Device: {device}")
                        slug += f"{device}:{command['command']},"
                        print(f"Slug: {slug}")
            slug = slug[:-1]
            path = f"hubs/harmony-hub/commandlist/{slug}"
    if not url:
        url = f"https://yo372002.ngrok.io/{path}"
    print(f"URL: {url}")
    response = send_request(url)
    result = {
        "response": response,
        "url": url
    }
    return result

def echo_device_name(handler_input):
    device_id = handler_input.request_envelope.context.system.device.device_id
    return echo_device_map.get(device_id, "unknown")

def dump_request(handler_input):
    intent_request = handler_input.request_envelope.request
    session_attributes = handler_input.attributes_manager.session_attributes
    print("Intent Request Object: " + json.dumps(to_dict(intent_request)))
    print("Session Attributes: " + json.dumps(session_attributes))

def camel_to_space(input_string, trim_last=False):
    result = ""
    for char in input_string:
        if char.isupper():
            result += " " + char.lower()
        else:
            result += char
    result = result.lstrip()
    if trim_last:
        result = result.split(' ')[:-1]
        result = ' '.join(result)
    return result
