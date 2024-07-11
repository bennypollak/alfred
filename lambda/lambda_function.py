# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type, is_intent_name

from ask_sdk_model import Response, Intent
from ask_sdk_model.dialog import DelegateDirective
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective, SpeakItemCommand)
from ask_sdk_model.ui import SimpleCard

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import lambda_defaults
import lambda_deprecated
import utils

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        user_name = 'Benny'
        session_attributes['user_name'] = user_name
        device_id = handler_input.request_envelope.context.system.device.device_id
        echo_device_name = utils.echo_device_name(handler_input)
        text = f"LaunchRequestHandler {user_name} Device name: {echo_device_name} Device ID: {device_id}"
        utils.s3_write(text)
        print(text)

        speak_output = utils.alfred_voice(f"Yes {user_name} on {echo_device_name}?")
        reprompt_output = utils.alfred_voice("Yes?")
        return (handler_input.response_builder.speak(speak_output)
                .set_card(SimpleCard(f"Alfred", f"Hi {user_name} how can I help you?"))
                .ask(reprompt_output).response
                )

class ScreenPowerIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ScreenPowerIntent")(handler_input)
    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        user_name = session_attributes['user_name']
        room_name, intended_room_name = utils.slot_value(handler_input, 'room')
        power, intended_power = utils.slot_value(handler_input, 'power', 'on')
        session_attributes['original_room_name'] = room_name
        session_attributes['intended_room_name'] = intended_room_name
        session_attributes['power'] = power
        if not room_name:
            speak_output = utils.alfred_voice("I didn't catch the room name. power for which room?")
            return handler_input.response_builder.speak(speak_output).ask(speak_output).response
        send_result = utils.send_tv_request(intended_room_name, 'onoff')
        speak_output = utils.alfred_voice(f"{user_name}, I did {intended_room_name} power {power} for {room_name} and got {send_result}")
        print(speak_output)
        return (handler_input.response_builder.speak(speak_output)
                .set_card(SimpleCard(f"Alfred", f"TV Power for {room_name}, got {send_result}"))
                .       response)

class ChannelIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ChannelIntent")(handler_input)
    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        user_name = session_attributes['user_name']
        room_name, intended_room_name = utils.slot_value(handler_input, 'room')
        if not room_name:
            speak_output = utils.alfred_voice("I didn't catch the room name. power for which room?")
            return handler_input.response_builder.speak(speak_output).ask(speak_output).response
        channel_number, intended_channel_number = utils.slot_value(handler_input, 'channel_number')
        station, intended_station = utils.slot_value(handler_input, 'station')
        if not channel_number and not station:
            speak_output = utils.alfred_voice("I didn't catch the channel?")
            return handler_input.response_builder.speak(speak_output).ask(speak_output).response
        intent_request = handler_input.request_envelope.request
        # print("ChannelIntent Request Object: " + json.dumps(utils.to_dict(intent_request)))
        session_attributes['channel_number'] = channel_number
        channel = channel_number if channel_number else station
        print(f"room {room_name} {intended_room_name}  Channel: {channel} Channel Number: {channel_number} and intended channel number: {intended_channel_number}")
        send_result = utils.send_channel_request(intended_room_name, channel_number, intended_station)
        speak_output = utils.alfred_voice(f"{user_name}, I did {intended_room_name} channel to {channel} for {room_name} and got {send_result}")
        print(speak_output)

        return (handler_input.response_builder.speak(speak_output)
                .set_card(SimpleCard(f"Alfred", f"Channel {channel} on {room_name}, got {send_result}"))
                .response)

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ScreenPowerIntentHandler())
sb.add_request_handler(ChannelIntentHandler())

lambda_deprecated.add_request_handlers(sb, logger)
# Must go at the end!
lambda_defaults.add_request_handlers(sb, logger)

lambda_handler = sb.lambda_handler()
