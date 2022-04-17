# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

#_____________________V1___________________
#_________ use of datetime with no consideration to daterange ___


from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from booking_details import BookingDetails


class Intent(Enum):
    #["BookFlight", "Greetings", "Confirmation"]
    BOOK_FLIGHT = "BookFlight"
    GREETINGS = "Greetings"
    CONFIRMATION = "Confirmation"
    #CANCEL = "Cancel"
    #GET_WEATHER = "GetWeather"
    #NONE_INTENT = "NoneIntent"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.BOOK_FLIGHT.value:
                result = BookingDetails()

                # We need to get the result from the LUIS JSON which at every level returns an array.

                departure_entities = recognizer_result.entities.get("$instance", {}).get( "Departure", [])
                if len(departure_entities) > 0:
                    result.origin = departure_entities[0]["text"].capitalize()
                    print("Departure ", result.origin)

                destination_entities = recognizer_result.entities.get("$instance", {}).get("Destination", [] )
                if len(destination_entities) > 0:
                    result.destination = destination_entities[0]["text"].capitalize()
                    print("Destination ", result.destination)

#                budget_entities = recognizer_result.entities.get("$instance", {}).get( "Budget", [])
#                budget_entities = recognizer_result.entities.get("$instance", {}).get( "money", [])
                budget_entities = recognizer_result.entities.get("money", [])
                if len(budget_entities) > 0:
                    result.number = budget_entities[0]["number"]
                    result.units = budget_entities[0]["units"]
                    result.budget = str(result.number)+" "+result.units
                    print("!Budget ", result.budget)                   
                    
                # This value will be a TIMEX. And we are only interested in a Date so grab the first result and drop
                # the Time part. TIMEX is a format that represents DateTime expressions that include some ambiguity.
                # e.g. missing a Year.

                departure_date_entities = recognizer_result.entities.get("$instance", {}).get( "DepartureDate", [])
                if len(departure_date_entities) > 0:
                    result.departure_date = departure_date_entities[0]["text"].capitalize()
                print("Departure Date ", result.departure_date)

                arrival_date_entities = recognizer_result.entities.get("$instance", {}).get( "ArrivalDate", [])
                if len(arrival_date_entities) > 0:
                    result.arrival_date =  arrival_date_entities[0]["text"].capitalize()
                print("Arrival Date ", result.arrival_date)   


        except Exception as exception:
            print(exception)

        return intent, result