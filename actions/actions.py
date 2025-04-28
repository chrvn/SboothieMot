# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class action_find_by_ingredient(Action):

    def name(self) -> Text:
        return "action_find_by_ingredient"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Load the CSV
        df = pd.read_csv('data/smoothies.csv')

        # Get the user's request
        requested_ingredient = next(tracker.get_latest_entity_values("ingredient"), None)
        
        if not requested_ingredient:
            dispatcher.utter_message(text="Please tell me an ingredient you're interested in.")
            return []

        # Find matching smoothies
        matching = df[df['Ingredients'].str.contains(requested_ingredient, case=False, na=False)]

        if matching.empty:
            dispatcher.utter_message(text=f"Sorry, I couldn't find a smoothie with {requested_ingredient}.")
        else:
            smoothie_names = matching['Recipe Name'].tolist()
            dispatcher.utter_message(text=f"I found these smoothies with {requested_ingredient}: {', '.join(smoothie_names)}")

        return []
