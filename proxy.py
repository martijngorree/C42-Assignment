from bottle import route, run, response
from c42 import C42Api
import json
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

try:
    from settings import *
except:
    raise Exception("You need a settings.py file with the C42_TOKEN var, see settings.default.py")

# TODO cache the entire call
@route("/events-with-subscriptions/<event_id>")
def events_with_subscriptions(event_id):
    api = C42Api(token=C42_TOKEN)

    events = api.request("events/{}".format(event_id)).get('data')
    event_subscriptions = api.request("event-subscriptions", { "event_ids": "[{}]".format(event_id) }).get('data')

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
