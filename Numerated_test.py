import Numerated
import unittest
import requests
from unittest.mock import MagicMock
from requests.compat import urljoin, quote_plus

BASE_URL = "https://api-v3.mbta.com/"
mock_resp_routes = [
        {
            "id":1,
            "attributes":{
                "direction_names": ["up","down"]
            }
        },
        {
            "id":2,
            "attributes":{
                "direction_names": ["left","right"]
            }
        }
        ]

class TestNumerated(unittest.TestCase):

    # Simple unit test section that may at most need mock data
    def test_generate_possible_options(self):
        self.assertEqual(Numerated.generate_possible_options(["1","2","3"]), "1\n2\n3\n", "Concating options correctly")
        self.assertEqual(Numerated.generate_possible_options(["1\n","2","3"]), "1\n\n2\n3\n", "Concating options correctly")

    def test_get_valid_routes(self):
        self.assertEqual(Numerated.get_valid_routes(mock_resp_routes), [1,2], "Should return all ids")

    def test_get_valid_directions(self):
        self.assertEqual(Numerated.get_valid_directions(mock_resp_routes, 1), ["up","down"], "Should return matching directions")
        self.assertEqual(Numerated.get_valid_directions(mock_resp_routes, 2), ["left","right"], "Should return matching directions")

    def test_parse_depart_time(self):
        self.assertEqual(str(Numerated.parse_depart_time("2021-03-22T17:45:34-04:00")), "2021-03-22 17:45:34", "Should be 6")

    # More involved tests that will require mocked method calls and returns from those calls that are fake

    def test_routes_data(self):
        # Here the entire test will be mocked method calls and we will only do assertions based
        # on what options are passed to methods
        requests.get = MagicMock(return_value=requests)
        requests.json = MagicMock(return_value={"data":"mocked out"})
        routes_params = dict(filter="0,1")
        ROUTES_END_POINT = urljoin(BASE_URL,quote_plus("routes"))
        val = Numerated.routes_data()
        requests.get.assert_called_with(ROUTES_END_POINT, params=routes_params)
        self.assertEqual(val, "mocked out")
        
    def test_get_valid_stops(self):
        # Here we need to stub out a response to the requests.get method and make assertions on what
        # options are passed to it
        stop = "Red"
        stop_params = dict(route=stop)
        requests.get = MagicMock(return_value=requests)
        requests.json = MagicMock(return_value={"data":[{"id":1, "val":"mocked out"}]})
        stop_end_point = Numerated.STOPS_END_POINT
        val = Numerated.get_valid_stops(stop)
        requests.get.assert_called_with(stop_end_point, params=stop_params)
        self.assertEqual(val, [1])

    def test_get_specific_stop(self):
        specific_stop_params = dict(route="Red", direction_id="up", id=1)
        requests.get = MagicMock(return_value=requests)
        requests.json = MagicMock(return_value={"data":[{"id":1, "val":"mocked out"}]})
        stop_end_point = Numerated.STOPS_END_POINT
        val = Numerated.get_specific_stop("Red", "up", 1)
        requests.get.assert_called_with(stop_end_point, params=specific_stop_params)
        self.assertEqual(val, {"id":1, "val":"mocked out"})

    def test_get_possible_predictions(self):
        get_specific_stop = MagicMock(return_value={"id":1, "val":"mocked out"})
        predictions_params = dict(stop=1,sort="departure_time")
        requests.get = MagicMock(return_value=requests)
        requests.json = MagicMock(return_value={"data":[{"id":1, "val":"mocked out"}]})
        val = Numerated.get_possible_predictions("Red", "up", 1)
        requests.get.assert_called_with(Numerated.PREDICTION_END_POINT, params=predictions_params)
        self.assertEqual(val, [{"id":1, "val":"mocked out"}])


    # Next section if I had more time would be the full mocking of method generic_user_input method and the main method
    # which both function as a kind of integration of our unit tested methods. Good practice would be to spend most
    # time on full test and senario coverage on unit tests foundation so these kind of integration tests can be
    # written more sparingly since require more time to create and are costly to standup.
    
if __name__ == '__main__':
    unittest.main()
    
