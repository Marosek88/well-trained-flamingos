import boto3
import json
import logging
import os
import urllib3

from datetime import datetime

logger = logging.getLogger()
log_level = logging.getLevelName(os.getenv("LOG_LEVEL", "INFO"))
logger.setLevel(log_level)


def post_joke():
    try:
        url="https://api.chucknorris.io/jokes/random"
        http = urllib3.PoolManager()
        raw_response = http.request('GET', url)
        response = json.loads(raw_response.data.decode('utf-8'))

        response_stringified = json.dumps(response, indent=4)
        encoded_string = response_stringified.encode("utf-8")

        now = datetime.utcnow()
        bucket_name = os.getenv("BUCKET")
        file_name = f"{now.strftime('%H-%M-%S')}.json"
        s3_path = f"chuck/{now.year}/{now.month}/{now.day}/{file_name}"

        s3 = boto3.resource("s3")
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)

        return {
            "statusCode": 200,
            "body": response_stringified
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": str(e)
        }