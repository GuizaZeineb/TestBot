# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


################################################################################################
#       Dialog to take into account the datetime difference between departure and arrival      #
################################################################################################

from datatypes_date_time.timex import Timex
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient

from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext
from botbuilder.dialogs.prompts import (
    DateTimePrompt,
    PromptValidatorContext,
    PromptOptions,
    DateTimeResolution,
)
from botbuilder.schema import InputHints
from .cancel_and_help_dialog import CancelAndHelpDialog


class ArrivalDateResolverDialog2(CancelAndHelpDialog):
    def __init__(self, 
                dialog_id: str = None, 
                telemetry_client: BotTelemetryClient = NullTelemetryClient(),):

        super(ArrivalDateResolverDialog2, self).__init__(
            dialog_id or ArrivalDateResolverDialog2.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client

        date_time_prompt = DateTimePrompt(
            DateTimePrompt.__name__, ArrivalDateResolverDialog2.datetime_prompt_validator
        )
        date_time_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__ + "2", [self.initial_step, self.final_step]
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(date_time_prompt)
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__ + "2"

    async def initial_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        timex = step_context.options
        prompt_msg_text = "Problem booking_details.arrival_date < booking_details.departure_date, for best results, please enter arrival date "
        prompt_msg = MessageFactory.text(
            prompt_msg_text, prompt_msg_text, InputHints.expecting_input
        )
        reprompt_msg_text = "I'm sorry, for best results, please enter your arrival travel date including the month, " \
                            "day and year. "
        reprompt_msg = MessageFactory.text(
            reprompt_msg_text, reprompt_msg_text, InputHints.expecting_input
        )


        if timex :    
            return await step_context.prompt(DateTimePrompt.__name__, PromptOptions(prompt=prompt_msg), )

        # We have a Date we just need to check it is unambiguous.
        if "definite" not in Timex(timex).types:
            # This is essentially a "reprompt" of the data we were given up front.
            return await step_context.prompt(
                DateTimePrompt.__name__, PromptOptions(prompt=reprompt_msg)
            )
        return await step_context.next(DateTimeResolution(timex=timex))

    async def final_step(self, step_context: WaterfallStepContext):
        timex = step_context.result[0].timex
        return await step_context.end_dialog(timex)

    @staticmethod
    async def datetime_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        if prompt_context.recognized.succeeded:
            timex = prompt_context.recognized.value[0].timex.split("T")[0]

            # TODO: Needs TimexProperty
            return "definite" in Timex(timex).types

        return False
