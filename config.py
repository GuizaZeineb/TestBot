#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

#_________________New Version takes into account the virtual environment  ______________

import os
from dotenv import load_dotenv

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """
    load_dotenv()
#    PORT = 49332 # if using env
    PORT = 3978  # if not using env
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")


    #_______________Nouveau Luis____________
#    LUIS_APP_ID = os.environ.get("LuisAppId", "e2c9e12a-31f4-4956-a89f-cc3fd548865d") # Random
    #LUIS_APP_ID = os.environ.get("LuisAppId", "9d603457-4956-484b-bcf6-ff2e6cd862b3")#Last good one
    LUIS_APP_ID = os.environ.get("LuisAppId", "fe2ea595-12f7-494c-8737-bc881341be54")# very last one for insights

#    LUIS_APP_ID = os.environ.get("LuisAppId", "af053a5d-6c77-4755-90a2-590d1044c0e6")

# #   Authoring Resource
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "p10luisresource-authoring.cognitiveservices.azure.com/")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "44680094d70f4b22bc6fb194086ee9f8")


    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "428b9636-5fe0-4eaa-8d34-7a0dec6c8a5e"
    )


#   Prediction Resource
#    LUIS_API_KEY = os.environ.get("LuisAPIKey", "5fc4ccbb7dc04aa094934613afb5f55f")
#    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "p10luisresource.cognitiveservices.azure.com/")


#Query = "book a flight on monday , march 28 from paris to london and return back on 30 march with 500£"
#    travel on 30/03/2022 and return on 30/04/2022 from Paris to London with 600£     #
#     fly to Geneva from Monaco on 30/03/2022 to 27/03/2022. It should cost less then -3000 €    #
#     traveling to: Sydney from: Paris on: 2022-04-13 returning on: 2022-04-30 with a maximum budget of: 4000 Euro.   #



# ##########     APP_Insights   #####
# traces
# | summarize count () by message
# | render piechart

# requests
# | where success == false
# | summarize failedCount=sum(itemCount), impactedUsers=dcount(user_Id) by operation_Name
# | order by failedCount desc