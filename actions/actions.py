import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import datetime
from typing import Any, Text, Dict, List

class ActionGetOpeningHours(Action):
    def name(self) -> str:
        return "action_get_opening_hours"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain) -> list:
        with open('opening_hours.json', 'r') as file:
            data = json.load(file)

        opening_hours = data.get('items', {})
        day = next(tracker.get_latest_entity_values("day"), None)
        
        def format_time(hour: int) -> str:
            return datetime.datetime.strptime(f"{hour}:00", "%H:%M").strftime("%I:%M %p")

        if day:
            day = day.strip().capitalize()

            if day in opening_hours:
                open_time = opening_hours[day]["open"]
                close_time = opening_hours[day]["close"]
                
                if open_time == 0 and close_time == 0:
                    dispatcher.utter_message(text=f"Sorry, we are closed on {day}.")
                else:
                    open_hour_str = format_time(open_time)
                    close_hour_str = format_time(close_time)
                    dispatcher.utter_message(
                        text=f"The opening hours on {day} are: {open_hour_str} to {close_hour_str}."
                    )
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find the opening hours for {day}.")
        else:
            hours_info = ""
            for day, times in opening_hours.items():
                open_time = times["open"]
                close_time = times["close"]
                if open_time == 0 and close_time == 0:
                    hours_info += f"{day}: Closed\n"
                else:
                    open_hour_str = format_time(open_time)
                    close_hour_str = format_time(close_time)
                    hours_info += f"{day}: {open_hour_str} to {close_hour_str}\n"
            
            dispatcher.utter_message(text=f"Our opening hours are as follows:\n{hours_info}")

        return [SlotSet("day", None)]

class ActionListMenu(Action):
    def name(self) -> str:
        return "action_list_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        menu = json.load(open('menu.json'))
        menu_items = [item["name"] for item in menu["items"]]
        dispatcher.utter_message(f"Our menu includes: {', '.join(menu_items[:-1])} and {menu_items[-1]}.")
        return []

class ActionPlaceOrder(Action):
    def name(self) -> Text:
        return "action_place_order"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        meal = tracker.get_slot("meal")
        menu = json.load(open('menu.json'))

        available_items = [item["name"].lower() for item in menu.get("items", [])]

        if meal.lower() in available_items:
            meal_item = next((item for item in menu["items"] if item["name"].lower() == meal.lower()), None)
        
            
            prep_time = meal_item["preparation_time"]
            now = datetime.datetime.now()
            ready_time = now + datetime.timedelta(hours=prep_time)
            ready_time_str = ready_time.strftime("%H:%M")
            response = f"You ordered a {meal}. Would you like any modifications?"
            dispatcher.utter_message(text=response)
            return [SlotSet("meal", meal), SlotSet("ready_time", ready_time_str)]
        else:
            dispatcher.utter_message(text=f"Sorry, we don't have {meal} on the menu. Please choose something else.")
            return [SlotSet("meal", None)]

class ActionAddModifications(Action):
    def name(self) -> str:
        return "action_add_modifications"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> list:
        modification = next(tracker.get_latest_entity_values("modification"), None)
        
        if modification and modification.lower() not in ["no", "no thank you"]:
            dispatcher.utter_message(text=f"Got it! I’ve added {modification} to your order. Is that all?")
            return [SlotSet("modification", modification)]
        else:
            dispatcher.utter_message(text="No modifications added. Is that all?")
            return [SlotSet("modification", None)]


class ActionFinalizeOrder(Action):
    def name(self) -> str:
        return "action_finalize_order"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        ready_time = tracker.get_slot("ready_time")
        
        entities = tracker.latest_message.get("entities", [])
        address_parts = [e["value"] for e in entities if e["entity"] == "delivery_address"]
        delivery_address = ", ".join(address_parts) if address_parts else tracker.get_slot("delivery_address")
        
        response = f"Great! Your order has been finalized and will be ready at {ready_time}. Your order will be delivered to {delivery_address}. Enjoy your meal!"
        
        dispatcher.utter_message(text=response)
        return []