# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
import s3
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type, is_intent_name, get_intent_name

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
        session_attributes['intent_name'] = "LaunchRequest"
        device_id = handler_input.request_envelope.context.system.device.device_id
        echo_device_name = utils.echo_device_name(handler_input)
        print(f'user_name {user_name} echo_device_name {echo_device_name}')
        text = f"LaunchRequestHandler {user_name} Device name: {echo_device_name} Device ID: {device_id}"
        s3.s3_write(text)
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
        intent_name = get_intent_name(handler_input)
        print(f"ScreenPowerIntent Intent Name: {intent_name}")
        power, intended_power = utils.slot_value(handler_input, 'power', 'on')
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes['intent_name'] = intent_name
        session_attributes['power'] = power
        room_name, intended_room_name = utils.slot_value(handler_input, 'room')
        if not room_name:
            room_name = intended_room_name = utils.room_echo_device_in(handler_input)
        if not room_name:
            device_name = utils.echo_device_name(handler_input)
            speak_output = utils.alfred_voice(f"power for which room from {device_name}?")
            return (handler_input.response_builder.speak(speak_output)
                    .speak(speak_output)
                    .add_directive(DelegateDirective(updated_intent=Intent(name="RoomIntent")))
                    .response
                    )
        session_attributes['original_room_name'] = room_name
        session_attributes['intended_room_name'] = intended_room_name
        return handle_request(handler_input, session_attributes)


class RoomIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("RoomIntent")(handler_input)
    def handle(self, handler_input):
        intent_name = get_intent_name(handler_input)
        print(f"RoomIntentHandler Intent Name: {intent_name}")
        session_attributes = handler_input.attributes_manager.session_attributes
        if not 'original_room_name' in session_attributes:
            room_name, intended_room_name = utils.slot_value(handler_input, 'room')
            session_attributes['original_room_name'] = room_name
            session_attributes['intended_room_name'] = intended_room_name
        return handle_request(handler_input, session_attributes)

class NextStepIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("NextStepIntent")(handler_input)
    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        original_room_name = session_attributes.get('original_room_name', 'unknown original room')
        intended_room_name = session_attributes.get('intended_room_name', 'unknown processed room')
        speak_output = utils.alfred_voice(f"I will take care of {original_room_name} as {intended_room_name} for you Benny")
        return handler_input.response_builder.speak(speak_output).set_should_end_session(True).response

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
        session_attributes['channel_number'] = channel_number
        session_attributes['intended_station'] = intended_station
        channel = channel_number if channel_number else station
        print(f"room {room_name} {intended_room_name}  Channel: {channel} Channel Number: {channel_number} and intended channel number: {intended_channel_number}")
        send_result = utils.send_channel_request(intended_room_name, channel_number, intended_station)
        speak_output = utils.alfred_voice(f"{user_name}, I did {intended_room_name} channel to {channel} for {room_name} and got {send_result}")
        print(speak_output)

        return (handler_input.response_builder.speak(speak_output)
                .set_card(SimpleCard(f"Alfred", f"Channel {channel} on {room_name}, got {send_result}"))
                .set_should_end_session(True).response)

def handle_request(handler_input, session_attributes):
    room_name = session_attributes.get('original_room_name')
    user_name = session_attributes.get('user_name')
    intent_name = session_attributes.get('intent_name')
    intent_name = utils.camel_to_space(intent_name)
    send_result = utils.send_generic_request(session_attributes)
    output_text = f"I did {intent_name} for {room_name} and got {send_result}"
    speak_output = utils.alfred_voice(output_text)
    print(output_text)
    return (handler_input.response_builder.speak(speak_output)
            .set_card(SimpleCard(f"Alfred", output_text))
            .set_should_end_session(True).response)

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ScreenPowerIntentHandler())
sb.add_request_handler(RoomIntentHandler())
sb.add_request_handler(ChannelIntentHandler())
sb.add_request_handler(NextStepIntentHandler())

lambda_deprecated.add_request_handlers(sb, logger)
# Must go at the end!
lambda_defaults.add_request_handlers(sb, logger)

lambda_handler = sb.lambda_handler()
