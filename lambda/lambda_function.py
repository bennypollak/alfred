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
import utils, configs

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        debug = s3.get_config().get('debug', True)
        user_name = 'Benny'
        session_attributes['user_name'] = user_name
        session_attributes['intent_name'] = "LaunchRequest"
        device_id = handler_input.request_envelope.context.system.device.device_id
        echo_device_name = utils.echo_device_name(handler_input)
        print(f'user_name {user_name} echo_device_name {echo_device_name}')
        text = f"LaunchRequestHandler {user_name} Device name: {echo_device_name} Device ID: {device_id}"
        s3.s3_write(text)
        print(text)

        speak_text = f"Yes {user_name} on {echo_device_name}?" if debug else f"Yes {user_name}?"
        speak_output = utils.alfred_voice(speak_text)
        reprompt_output = utils.alfred_voice("Yes?")
        return (handler_input.response_builder.speak(speak_output)
                .set_card(SimpleCard(f"Alfred", f"Hi {user_name} how can I help you?"))
                .ask(reprompt_output).response
                )

class SetConfigIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SetConfigIntent")(handler_input)
    def handle(self, handler_input):
        intent_request = handler_input.request_envelope.request
        session_attributes = handler_input.attributes_manager.session_attributes
        original_debug, intended_debug = utils.slot_value(handler_input, 'on_off')
        config = s3.get_config()
        config['debug'] = True if intended_debug == 'on' else False
        s3.write_config(config)
        speak_text = f"setting intended_debug {intended_debug} original_debug: {original_debug}"
        speak_output = utils.alfred_voice(speak_text)
        return (handler_input.response_builder.speak(speak_output)
            .set_card(SimpleCard(f"Alfred", speak_text))
            .set_should_end_session(True).response)

class ScreenPowerIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ScreenPowerIntent")(handler_input)
    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes['intent_name'] = get_intent_name(handler_input)
        session_attributes['action'] = 'tv-power'
        power, intended_power = utils.slot_value(handler_input, 'power', 'toggle')
        print(f"Power: {power}, Intended Power: {intended_power}")
        session_attributes['power'] = power
        session_attributes['intended_power'] = intended_power
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
        # output_text = f"Power: {power}, Intended Power: {intended_power}, Room Name: {room_name}, Intended Room Name: {intended_room_name}"
        # speak_output = utils.alfred_voice(output_text)
        # print(output_text)
        # return (handler_input.response_builder.speak(speak_output)
        #         .set_card(SimpleCard(f"Alfred", f"Power: {power}, Intended Power: {intended_power}"))
        #         .set_should_end_session(False).response)
        # print(f"Room Name: {room_name}, Intended Room Name: {intended_room_name}")
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

class ChannelIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ChannelIntent")(handler_input)
    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        debug = session_attributes['debug']
        session_attributes['intent_name'] = get_intent_name(handler_input)
        session_attributes['action'] = 'channel'
        channel_number, intended_channel_number = utils.slot_value(handler_input, 'channel_number')
        station, intended_station = utils.slot_value(handler_input, 'station')
        if not channel_number and not station:
            speak_output = utils.alfred_voice("I didn't catch the channel")
            return handler_input.response_builder.speak(speak_output).ask(speak_output).response
        session_attributes['channel_number'] = channel_number
        session_attributes['intended_station'] = intended_station
        room_name, intended_room_name = utils.slot_value(handler_input, 'room')
        if not room_name:
            room_name = intended_room_name = utils.room_echo_device_in(handler_input)
        if not room_name:
            device_name = utils.echo_device_name(handler_input)
            speak_output = utils.alfred_voice(f"channel for which room from {device_name}?")
            return (handler_input.response_builder.speak(speak_output)
                    .speak(speak_output)
                    .add_directive(DelegateDirective(updated_intent=Intent(name="RoomIntent")))
                    .response
                    )
        session_attributes['original_room_name'] = room_name
        session_attributes['intended_room_name'] = intended_room_name
        return handle_request(handler_input, session_attributes)

class ScreenActionIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ScreenActionIntent")(handler_input)
    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes['intent_name'] = get_intent_name(handler_input)
        user_name = session_attributes['user_name']
        action, intended_action = utils.slot_value(handler_input, 'action')
        session_attributes['action'] = action
        session_attributes['intended_action'] = intended_action
        room_name, intended_room_name = utils.slot_value(handler_input, 'room')
        if not room_name:
            room_name = intended_room_name = utils.room_echo_device_in(handler_input)
        if not room_name:
            device_name = utils.echo_device_name(handler_input)
            speak_output = utils.alfred_voice(f"action for which room from {device_name}?")
            return (handler_input.response_builder.speak(speak_output)
                    .speak(speak_output)
                    .add_directive(DelegateDirective(updated_intent=Intent(name="RoomIntent")))
                    .response
                    )
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
        speak_output = utils.alfred_voice(f"I will take care of {original_room_name} as {intended_room_name}")
        return handler_input.response_builder.speak(speak_output).set_should_end_session(True).response


def handle_request(handler_input, session_attributes):
    room_name = session_attributes.get('original_room_name')
    user_name = session_attributes.get('user_name')
    intent_name = session_attributes.get('intent_name')
    intent_name = utils.camel_to_space(intent_name)
    send_result = utils.process_request(session_attributes)
    output_text = f"I did {intent_name} for {room_name} and got {send_result}"
    speak_output = utils.alfred_voice(output_text)
    print(output_text)
    return (handler_input.response_builder.speak(speak_output)
            .set_card(SimpleCard(f"Alfred", output_text))
            .set_should_end_session(True).response)

class JustSayIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("WhyAlfredIntent")(handler_input) or is_intent_name("WhyAlfredMoreIntent")(handler_input)
    def handle(self, handler_input):
        intent_request = handler_input.request_envelope.request
        session_attributes = handler_input.attributes_manager.session_attributes
        next_intent = session_attributes.get('next_intent')

        intent_name = get_intent_name(handler_input)
        say_request_response = configs.say_request_responses.get(intent_name)
        speak_text = say_request_response.get('text', "I don't know")
        speak_output = utils.alfred_voice(speak_text)
        more_text = say_request_response.get('next_text')
        next_intent = say_request_response.get('next_intent')
        if not next_intent:
            return (handler_input.response_builder.speak(speak_output)
                    .set_card(SimpleCard(f"Alfred", speak_text))
                    .set_should_end_session(True).response)
        speak_text += f" {more_text}"
        session_attributes['next_intent'] = next_intent

        return (handler_input.response_builder.speak(speak_output)
                .speak(speak_output)
                .set_card(SimpleCard(f"Alfred", speak_text))
                .add_directive(DelegateDirective(updated_intent=Intent(name="YesNoIntent")))
                .response
                )
class YesNoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("YesNoIntent")(handler_input)
    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        next_intent = session_attributes['next_intent']
        yes_no, intended_yes_no = utils.slot_value(handler_input, 'yes_no')

        if yes_no == 'yes':
            return (handler_input.response_builder
                    .speak('')
                    .add_directive(DelegateDirective(updated_intent=Intent(name=next_intent)))
                    .response
                    )
        else:
            speak_text = "Ok. Goodbye."
            speak_output = utils.alfred_voice(speak_text)
            return (handler_input.response_builder.speak(speak_output)
                    .set_card(SimpleCard(f"Alfred", speak_text))
                    .set_should_end_session(True).response)


sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ScreenPowerIntentHandler())
sb.add_request_handler(SetConfigIntentHandler())
sb.add_request_handler(ScreenActionIntentHandler())
sb.add_request_handler(RoomIntentHandler())
sb.add_request_handler(ChannelIntentHandler())
sb.add_request_handler(NextStepIntentHandler())
sb.add_request_handler(JustSayIntentHandler())
sb.add_request_handler(YesNoIntentHandler())

lambda_deprecated.add_request_handlers(sb, logger)
# Must go at the end!
lambda_defaults.add_request_handlers(sb, logger)

lambda_handler = sb.lambda_handler()
