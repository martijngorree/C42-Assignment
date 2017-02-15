from functools import partial
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
    """
    Simple C42 Api wrapper.
    You should be able to call the api with:

        api = C42Api(token=<yourtoken>)

        api.get(<api_method>, params={ <url params> })
        api.post(<api_method>, data={ <post data> })
        api.put(<api_method, data={ <data> })
        api.delete(<api_method>)
    """

    def __init__(self, token=None):
        self.token = token
        self.allowed_methods = ['get', 'put', 'post', 'delete', 'patch']

    def __getattr__(self, method):
        if method in self.allowed_methods:
            return partial(self._request, method=method)
        else:
            raise Exception("Trying to call non-existing method {}".format(method))

    def _fix_params(self, params):
        """
        Compensate for the weird way the c42 api expects lists in url params.
        So: passing { 'items': ['1','2'] } resulting in "?items=1&items=2"
        We should get: ?items=[1,2]
        -> http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
        """
        for key,value in params.items():
            if isinstance(value, list):
                value = "[{}]".format(",".join(value))
                params[key] = value

        return params

    def _url(self, path):
        """
        return the full api url
        """
        return "{}/{}/".format(API_URL, path)

    def _request(self, *args, **kwargs):
        """
        Do the actual api request with authorisation token
        """

        http_call_type = kwargs.pop('method')
        request_method = getattr(requests, http_call_type)
        api_method = args[0]

        headers = {
            "Authorization": "Token {}".format(self.token)
            }
        kwargs['headers'] = headers
        if 'params' in kwargs.keys():
            kwargs['params'] = self._fix_params(kwargs['params'])

        logging.debug([api_method, kwargs])

        response = request_method(url=self._url(api_method), **kwargs)
        return response.json()

if __name__ == "__main__":
    """
    Test the api
    """
    api = C42Api(token=C42_TOKEN)
    EVENT_ID = "704ec81389b26f30452f314845e8e0ad_14866401158750"

    logging.debug(api.get("events/{}".format(EVENT_ID)))
    logging.debug(api.get("event-subscriptions", params={ "event_ids": "[{}]".format(EVENT_ID) }))
    

