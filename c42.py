import requests
import logging

try:
    from settings import *
except:
    raise Exception("You need a settings.py file with the C42_TOKEN var, see settings.default.py")

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
API_URL = "https://demo.calendar42.com/api/v2"

class C42Api:
    def __init__(self, token=None):
        self.token = token

    def _url(self, path):
        return "{}/{}/".format(API_URL, path)

    def request(self, path, params=None):
        headers = {
            "Authorization": "Token {}".format(self.token)
            }
        response = requests.get(url=self._url(path), params=params, headers=headers)
        logging.debug(response.url)
        return response.json() 

if __name__ == "__main__":

    api = C42Api(token=C42_TOKEN)
    EVENT_ID = "704ec81389b26f30452f314845e8e0ad_14866401158750"

    print(api.request("events/{}".format(EVENT_ID)))
    # TODO: Check if passing url params as "[item, item]" is actually valid.
    print(api.request("event-subscriptions", { "event_ids": "[{}]".format(EVENT_ID) }))
    

