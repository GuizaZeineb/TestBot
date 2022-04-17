# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


#_ vesion with budget and datetime tests


from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from botbuilder.schema import InputHints
from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog
from .arrival_date_resolver_dialog import ArrivalDateResolverDialog
from .arrival_date_resolver_dialog2 import ArrivalDateResolverDialog2

class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""
    def __init__(self, dialog_id: str = None,  telemetry_client: BotTelemetryClient = NullTelemetryClient(),):
        super(BookingDialog, self).__init__(dialog_id or BookingDialog.__name__, telemetry_client)
        
        self.telemetry_client = telemetry_client
        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = telemetry_client

        self.add_dialog(text_prompt)
#        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(DateResolverDialog(DateResolverDialog.__name__, self.telemetry_client))
        self.add_dialog(ArrivalDateResolverDialog(ArrivalDateResolverDialog.__name__, self.telemetry_client))
        self.add_dialog(ArrivalDateResolverDialog2(ArrivalDateResolverDialog2.__name__, self.telemetry_client))

        
        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.destination_step,
                    self.origin_step,
                    self.departure_date_step,
                    self.arrival_date_step,
                    self.error_date_step,
                    self.budget_step,
                    self.confirm_step,
                    self.final_step,
            ],
        ) 
        
        waterfall_dialog.telemetry_client = telemetry_client
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a destination city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        if booking_details.destination is None:
            message_text = "Where would you like to travel to?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(booking_details.destination)


    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        If an origin city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.destination = step_context.result
        if booking_details.origin is None:
            message_text = "From what city will you be travelling?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(booking_details.origin)



    async def departure_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a travel date has not been provided, prompt for one.
        This will use the DATE_RESOLVER_DIALOG.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.origin = step_context.result
        if not booking_details.departure_date or self.is_ambiguous(
            booking_details.departure_date
        ):
            return await step_context.begin_dialog(
                DateResolverDialog.__name__, booking_details.departure_date
            )
        return await step_context.next(booking_details.departure_date)


    async def arrival_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a travel date has not been provided, prompt for one.
        This will use the Arrival_DATE_RESOLVER_DIALOG.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.departure_date = step_context.result
        if not booking_details.arrival_date or self.is_ambiguous(
            booking_details.arrival_date 
        ):
            return await step_context.begin_dialog(
                ArrivalDateResolverDialog.__name__, booking_details.arrival_date
            )
        return await step_context.next(booking_details.arrival_date)


    async def error_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a travel date has not been provided, prompt for one.
        This will use the Arrival_DATE_RESOLVER_DIALOG.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.arrival_date = step_context.result
        print("____booking_details.arrival_date", booking_details.arrival_date)
        print("____booking_details.departure_date ", booking_details.departure_date)
        
        if booking_details.arrival_date < booking_details.departure_date:
            print("____problem booking_details.arrival_date < booking_details.departure_date____")
#            ___________________Add   Test____________
            return await step_context.begin_dialog(
                ArrivalDateResolverDialog2.__name__, booking_details.arrival_date
            )

            # reprompt_msg_text2 = "Problem booking_details.arrival_date < booking_details.departure_date, for best results, please enter arrival date "
            # reprompt_msg2 = MessageFactory.text(
            #     reprompt_msg_text2, reprompt_msg_text2, InputHints.expecting_input
            # )
            # return await step_context.prompt(
            #     TextPrompt.__name__, PromptOptions(prompt=reprompt_msg2)
            # )  

        return await step_context.next(booking_details.arrival_date)



    async def budget_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        If a budget has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.arrival_date = step_context.result

# #_________________Add money test_________________
        pb = False
        message_text = None
        if booking_details.budget[0] is None:
            message_text = "What is your maximum budget?"
            pb = True
        elif type(booking_details.number) is not tuple:
             if booking_details.number <= 0:
                 message_text = "The budget must be positive !" 
                 pb = True 
        # elif (booking_details.number is not None) and booking_details.number <= 0:
        #     message_text = "The budget must be positive !"   
        #     pb = True 

        if pb :
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )


        return await step_context.next(booking_details.budget)
#     async def budget_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
#         """
#         If a budget has not been provided, prompt for one.
#         :param step_context:
#         :return DialogTurnResult:
#         """
#         booking_details = step_context.options

#         # Capture the response to the previous step's prompt
#         booking_details.arrival_date = step_context.result

# # #_________________Add money test_________________
#         pb1, pb2 = False, False
#         if booking_details.budget[0] is None:
#             message_text1 = "What is your maximum budget?"
#             pb1 = True
#         elif type(booking_details.number) is not tuple:
#              if booking_details.number <= 0:
#                  message_text2 = "The budget must be positive !" 
#                  pb2 = True 
#         # elif (booking_details.number is not None) and booking_details.number <= 0:
#         #     message_text = "The budget must be positive !"   
#         #     pb = True 

#         if pb1 :
#             prompt_message = MessageFactory.text(
#                 message_text1, message_text1, InputHints.expecting_input
#             )
#             return await step_context.prompt(
#                 TextPrompt.__name__, PromptOptions(prompt=prompt_message)
#             )
#         if pb2 :
#             prompt_message = MessageFactory.text(
#                 message_text2, message_text2, InputHints.expecting_input
#             )
#             return await step_context.prompt(
#                 TextPrompt.__name__, PromptOptions(prompt=prompt_message))

#         return await step_context.next(booking_details.budget)


    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        Confirm the information the user has provided.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.budget = step_context.result
        message_text = (
            f"Please confirm, I have you traveling to: { booking_details.destination } from: "
            f"{ booking_details.origin } on: { booking_details.departure_date} returning on: "
            f"{booking_details.arrival_date} with a maximum budget of: {booking_details.budget}."
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        properties = {}
        properties["Destination"] = booking_details.destination
        properties["Departure"] = booking_details.origin
        properties["DepartureDate"] = booking_details.departure_date
        properties["ArrivalDate"] = booking_details.arrival_date
        properties["Budget"] = booking_details.budget

        # severity levels as per  App Insight doc
        severity_level = {0: "Verbose",
                          1: "Information",
                          2: "Warning",
                          3: "Error",
                          4: "Critical",
                        }

        if step_context.result:
            # booking_details = step_context.options

            # TRACK THE DATA INTO Application INSIGHTS
            # INFO, ERROR are severity levels reported to App Insight
            self.telemetry_client.track_trace("GOOD answer", properties, severity_level[1])
            self.telemetry_client.flush()
            return await step_context.end_dialog(booking_details)
        else:
            # TRACK THE DATA INTO Application INSIGHTS
            self.telemetry_client.track_trace("BAD answer", properties, severity_level[3]) 
            self.telemetry_client.flush()          

        return await step_context.end_dialog()

    def is_ambiguous(self, timex: str) -> bool:
        timex_property = Timex(timex)
        return "definite" not in timex_property.types

