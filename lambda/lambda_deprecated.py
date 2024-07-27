# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
import requests

import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type, is_intent_name

from ask_sdk_model import Response, Intent
from ask_sdk_model.dialog import DelegateDirective
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective, SpeakItemCommand)
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective

logger = logging.getLogger(__name__)
import utils

class TestIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("TestIntent")(handler_input)
    def handle(self, handler_input):
        movie_name = "laWRENCE of arabia" #handler_input.request_envelope.request.intent.slots["movie_name"].value
        speak_output = f"Playing {movie_name} on Fire TV."

        # Fire TV directive to play the movie (using RenderDocumentDirective)
        document = {
            # ... (APL document structure)
            "mainTemplate": {
                "items": [
                    {
                        "type": "FireTvVideo",
                        "source": f"https://www.amazon.com/dp/{movie_name}", # Replace with your video source
                        "autoplay": True,
                    }
                ]
            }
        }

        return (
            handler_input.response_builder
            .speak(speak_output)
            .add_directive(
                RenderDocumentDirective(
                    token="videoPlayerToken",
                    document=document,
                )
            )
            .response
        )
        intent_request = handler_input.request_envelope.request
        session_attributes = handler_input.attributes_manager.session_attributes
        print("Intent Request Object: " + json.dumps(utils.to_dict(intent_request)))
        original_room_name, intended_room_name = utils.slot_value(handler_input, 'room')
        if not original_room_name:
            speak_output = utils.alfred_voice("I didn't catch the room name. power for which room")
            print("No room name received")
            return handler_input.response_builder.speak(speak_output).ask(speak_output).response
        speak_output = utils.alfred_voice(f"Processing the room name: {original_room_name} as {intended_room_name} Moving to the next step.")
        session_attributes['original_room_name'] = original_room_name
        session_attributes['intended_room_name'] = intended_room_name
        return (handler_input.response_builder.speak(speak_output)
            .add_directive(DelegateDirective(updated_intent=Intent(name="TestNextStepIntent")))
            .response)

class TestNextStepIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("TestNextStepIntent")(handler_input)
    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        original_room_name = session_attributes.get('original_room_name', 'unknown original room')
        intended_room_name = session_attributes.get('intended_room_name', 'unknown processed room')
        speak_output = utils.alfred_voice(f"I will take care of {original_room_name} as {intended_room_name} for you Benny")
        return handler_input.response_builder.speak(speak_output).set_should_end_session(True).response

def add_request_handlers(sb, _logger=logger):
    global logger
    logger = _logger

    sb.add_request_handler(TestIntentHandler())
    sb.add_request_handler(TestNextStepIntentHandler())
