# -*- coding: utf-8 -*-

# This is a AC Remote Controller for Alexa Skill, built using
# the decorators approach in skill builder.
# By: Javier CORDON
# August 17th, 2023
# Based on Hello Alexa sample from AWS.

import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils.request_util import get_slot
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

import boto3
import json

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_thing_state(thingName):
    client = boto3.client('iot-data', region_name='us-west-1')
    response = client.get_thing_shadow(thingName=thingName)

    streamingBody = response["payload"]
    jsonState = json.loads(streamingBody.read())

    return jsonState
    
def set_thing_ir_cmd(thingName, state):
    # Change topic, qos and payload
    client = boto3.client('iot-data', region_name='us-west-1')
    payload = json.dumps({'state': { 'desired': { 'ir_cmd': { 'onboard': state } } }})

    logger.info("IOT update, thingName:"+thingName+", payload:"+payload)

    response = client.update_thing_shadow(
        thingName = thingName, 
        payload =  payload
        )

    logger.info("IOT response: " + str(response))  
    logger.info("Body:"+ str(response['payload'].read()))
    return response['payload'].read()
    
@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text)).set_should_end_session(
        False).response


@sb.request_handler(can_handle_func=is_intent_name("HelloWorldIntent"))
def hello_world_intent_handler(handler_input):
    """Handler for Hello World Intent."""
    # type: (HandlerInput) -> Response
    print("Entering Intent Hello World")
    speech_text = "Hello. This is a project developed while studying in K.I.C."

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text)).set_should_end_session(
        True).response
        
@sb.request_handler(can_handle_func=is_intent_name("coldTemperature"))
def coldTemperature_handler(handler_input):
    """Handler for Set Cold Temperature in AC"""
    # type: (HandlerInput) -> Response
    print("Entering Intent Cold Temperature")
    slots = get_slot(handler_input, 'temperature')
    tempVal = float(slots.value)
    tempValString = "{:.1f}".format(tempVal)
    
    thingName = "remotePrototype01"
    
    shadow = get_thing_state(thingName)
    shadowReported = shadow["state"]["reported"]
    shadowRTemperature = shadowReported["ir_cmd"]["onboard"]
    print("Current IR CMD State", shadowRTemperature)
    
    state = f"coldAuto_{tempValString}.py"
    rPayload = set_thing_ir_cmd(thingName, state)
    
    speech_text = f"Ok. Temperature set to {tempValString}"
    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Cold Temperature set", speech_text)).set_should_end_session(
        True).response

@sb.request_handler(can_handle_func=is_intent_name("turnOffAC"))
def turnOffAC_handler(handler_input):
    """Handler to turn off AC"""
    
    thingName = "remotePrototype01"
    
    shadow = get_thing_state(thingName)
    shadowReported = shadow["state"]["reported"]
    shadowRTemperature = shadowReported["ir_cmd"]["onboard"]
    print("Current IR CMD State", shadowRTemperature)
    
    state = f"stop.py"
    rPayload = set_thing_ir_cmd(thingName, state)
    
    speech_text = f"Ok. AC is about to turn off."
    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Turn Off AC", speech_text)).set_should_end_session(
        True).response

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "You can say hello to me!"

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            "Hello World", speech_text)).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Goodbye!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The Hello World skill can't help you with that.  "
        "You can say hello!!")
    reprompt = "You can say hello!!"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


lambda_handler = sb.lambda_handler()
