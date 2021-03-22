import requests
from requests.compat import urljoin, quote_plus
import json
import os
import datetime


BASE_URL = "https://api-v3.mbta.com/"
ROUTES_END_POINT = urljoin(BASE_URL,quote_plus("routes"))
STOPS_END_POINT = urljoin(BASE_URL,quote_plus("stops"))
PREDICTION_END_POINT = urljoin(BASE_URL,quote_plus("predictions"))
FIRST_ROUTE_SELECT_MSG = "What route would you like to pick from:"
FIRST_STOP_SELECT_MSG = "What stop would you like to pick from:"
FIRST_DIRECTION_SELECT_MSG = "What direction would you like to travel from:"


def generate_possible_options(options_arr):
    opt_string = ""
    for opt in options_arr:
        opt_string += opt.lower() + "\n"
    return opt_string

def generic_user_input(input_request, options):
    valid_selection = False
    prompt = input_request
    possible_options = {x.lower() for x in options}
    mapping = {x.lower():x for x in options}
    possible_options_str = generate_possible_options(options)
    selected_option = ""
    while not valid_selection:
        selected_option = input(prompt+"\n"+possible_options_str).lower()
        if selected_option in possible_options:
            selected_option = mapping[selected_option]
            valid_selection = True
        else:
            prompt = "Makes sure to select from valid options. "+input_request
    return selected_option

def print_json_debug(json_str):
    print(json.dumps(json_str, indent=6))

def routes_data():
    routes_params = dict(filter="0,1")
    resp_routes = requests.get(ROUTES_END_POINT, params=routes_params)
    resp_routes_json = resp_routes.json()["data"]
    return resp_routes_json

def get_valid_routes(resp_routes_json):
    route_ids = [x["id"] for x in resp_routes_json]
    return route_ids

def get_valid_directions(resp_routes_json, route):
    directions = [ x["attributes"]["direction_names"] for x in resp_routes_json if x["id"]==route][0]
    return directions

def get_valid_stops(route):
    stop_params = dict(route=route)
    resp_stops = requests.get(STOPS_END_POINT, params=stop_params).json()["data"]
    possible_stops = [x["id"] for x in resp_stops]
    return possible_stops

def get_prediction_depart_time(route, direction, stop):
    specific_stop_params = dict(route=route, direction_id=direction, id=stop)
    specific_stop = requests.get(STOPS_END_POINT, params=specific_stop_params).json()["data"][0]
    predictions_params = dict(stop=specific_stop["id"],sort="departure_time")
    resp_predictions =  requests.get(PREDICTION_END_POINT, params=predictions_params).json()["data"]
    resp_predictions= [x for x in resp_predictions if x["attributes"]["departure_time"] != None]
    next_depart = resp_predictions[0]["attributes"]["departure_time"]
    return next_depart

def parse_depart_time(depart_str):
    return datetime.datetime.strptime(depart_str,"%Y-%m-%dT%H:%M:%S-04:00")

def main():
    # Get valid routes
    resp_routes_json = routes_data()
    route_ids = get_valid_routes(resp_routes_json)
    # Prompt user to select a route
    route = generic_user_input(FIRST_ROUTE_SELECT_MSG, route_ids)
    print("you selected: "+route)

    # Get valid stops based on what the user selected
    possible_stops = get_valid_stops(route)
    # Prompt user to select a stop
    stop = generic_user_input(FIRST_STOP_SELECT_MSG, possible_stops)
    print("you selected: "+stop)

    # Get valid directions based on user route selection
    directions = get_valid_directions(resp_routes_json, route)
    # Prompt user to select a valid route
    direction = generic_user_input(FIRST_DIRECTION_SELECT_MSG, directions)
    print("you selected: "+direction)

    # Based on all user input up to here query to see if we can find the next non-null depart time
    # for this stop, going in this direction
    next_depart = get_prediction_depart_time(route, direction, stop)
    depart_time = parse_depart_time(next_depart)
    print("your earliest predicted departure is at: ",depart_time)

if __name__ == "__main__":
    main

