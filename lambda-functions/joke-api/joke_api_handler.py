import logging

from get_joke import get_joke, get_jokes
from post_joke import post_joke

logger = logging.getLogger()
log_level = logging.getLevelName("INFO")
logger.setLevel(log_level)


def lambda_handler(event, context):
    logger.info(f"event: {event}")

    resource = event.get("resource", "")
    method = event.get("httpMethod", "")

    if resource == "/jokes":
        if method == "POST":
            return post_joke()

        elif method == "GET":
            return get_jokes()

        else:
            return {"statusCode": 405, "body": f"Method {method} not allowed."}
    elif resource == "/jokes/{joke_id}":
        if method == "GET":
            joke_id = event["pathParameters"]["joke_id"]
            return get_joke(joke_id)
        else:
            return {"statusCode": 405, "body": f"Method {method} not allowed."}

    else:
        return {"statusCode": 404, "body": f"Resource {resource} not found."}
