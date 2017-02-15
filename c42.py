import requests
import logging

# TODO: Clean up, should be in one place
try:
    from settings import *
except:
    raise Exception("You need a settings.py file with the C42_TOKEN var, see settings.default.py")

# TODO: Clean this up, should be in one place.
if DEBUG:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.ERROR)

API_URL = "https://demo.calendar42.com/api/v2"

class C42Api:
    def __init__(self, token=None):
        self.token = token

    def _url(self, path):
        return "{}/{}/".format(API_URL, path)

    # TODO: Only handles GET requests, needs to handle all
    def request(self, path, params=None):
        headers = {
            "Authorization": "Token {}".format(self.token)
            }
        response = requests.get(url=self._url(path), params=params, headers=headers)
        return response.json()

if __name__ == "__main__":

    api = C42Api(token=C42_TOKEN)
    EVENT_ID = "704ec81389b26f30452f314845e8e0ad_14866401158750"

    logging.debug(api.request("events/{}".format(EVENT_ID)))
    # TODO: Check if passing url params as "[item, item]" is actually valid. Because it is kind of ugly.
    # http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    logging.debug(api.request("event-subscriptions", { "event_ids": "[{}]".format(EVENT_ID) }))
    

