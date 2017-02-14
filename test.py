import unittest
import requests

class TestProxy(unittest.TestCase):

    def test_event_subscriptions(self):

        event_id = "704ec81389b26f30452f314845e8e0ad_14866401158750"
        response = requests.get("http://localhost:8080/events-with-subscriptions/{}".format(event_id))

        self.assertEqual(response.json(), {
            "names": ['API', 'Michel', 'Jasper', 'Bob', 'Dennis', 'Edmon'], 
            "id": '704ec81389b26f30452f314845e8e0ad_14866401158750', 
            "title": 'Drink a cup of coffee with C42 Team',
            })


if __name__ == "__main__":
    unittest.main()
