import Numerated
import unittest

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
        pass
    def test_get_valid_stops(self):
        # Here we need to stub out a response to the requests.get method and make assertions on what
        # options are passed to it
        pass
    def test_get_prediction_depart_time(self):
        # Here we need to stub out two reponses to the request.get method and additionally make assertions
        # on the returned obj
        pass

    # Next section if I had more time would be the full mocking of method generic_user_input method and the main method
    # which both function as a kind of integration of our unit tested methods. Good practice would be to spend most
    # time on full test and senario coverage on unit tests foundation so these kind of integration tests can be
    # written more sparingly since require more time to create and are costly to standup.
    
if __name__ == '__main__':
    unittest.main()
    
