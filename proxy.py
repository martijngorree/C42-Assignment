# TODO: Make it a real proxy, pass "normal" requests to the C42 api

from bottle import route, run, response
from c42 import C42Api
from memcache import Client

import json
import logging
import hashlib

# TODO: Clean up
try:
    from settings import *
except:
    raise Exception("You need a settings.py file with the C42_TOKEN var, see settings.default.py")

# TODO: Clean up
if DEBUG:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.ERROR)


api = C42Api(token=C42_TOKEN)
mc = Client(MEMCACHED_SERVERS, debug=DEBUG)
try:
    mc.get_stats()
except:
    raise

def cached_request(method, *args, **kwargs):
    """
    Cache the requests to the API.
    More or less a wrapper for the api.request call
    """

    # build a caching key hash based on the whole request.
    # basicly just flatten out all the data and create a hash
    cache_key = str("{}{}{}".format(method, json.dumps(args), json.dumps(kwargs))).encode('utf-8')
    logging.debug("Generated cache_key: {}".format(cache_key))
    hashed_cache_key = hashlib.md5(cache_key).hexdigest()
    logging.debug("Hashed key: {}".format(hashed_cache_key))

    try:
        logging.debug("Hitting cache for {}".format(method))
        response = mc.get(hashed_cache_key)
        if response == None:
            raise Exception("No cached response found")
    except:
        response = api.request(method, *args, **kwargs)
        mc.set(hashed_cache_key, response, time=MEMCACHED_TTL)

    return response

# TODO: call should be "event-with-subscriptions" not plural, since its one event
# TODO: security? Implement a token, just like the c42 api
@route("/events-with-subscriptions/<event_id>")
def events_with_subscriptions(event_id):

    events = cached_request("events/{}".format(event_id)).get('data')
    event_subscriptions = cached_request("event-subscriptions", { "event_ids": "[{}]".format(event_id) }).get('data')

    logging.debug(events)
    logging.debug(event_subscriptions)

    event_title = events[0].get('title')
    event_id = events[0].get('id')
    subscribers = [subscription['subscriber']['first_name'] for subscription in event_subscriptions]

    data = {
        "id": event_id,
        "title": event_title,
        "names": subscribers,
        }
    response.content_type = "application/json"
    return json.dumps(data)

if __name__ == "__main__":
    run(host=PROXY_HOST, port=PROXY_PORT, debug=DEBUG)
