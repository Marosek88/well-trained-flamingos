import boto3
import json
import logging
import os

logger = logging.getLogger()
log_level = logging.getLevelName(os.getenv("LOG_LEVEL", "INFO"))
logger.setLevel(log_level)


def get_jokes():
    try:
        s3 = boto3.resource("s3")
        bucket_name = os.getenv("BUCKET")
        joke_bucket = s3.Bucket(bucket_name)

        joke_list = [joke.key for joke in joke_bucket.objects.all()]

        return {
            "statusCode": 200,
            "body": json.dumps(joke_list)
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": str(e)
        }


def get_joke(joke_id: str):
    try:
        id_split = joke_id.split("-")
        if len(id_split) != 6:
            return {
                "statusCode": 400,
                "body": "Invalid joke_id"
            }

        bucket_name = os.getenv("BUCKET")
        file_name = f"{id_split[3]}-{id_split[4]}-{id_split[5]}.json"
        s3_path = f"chuck/{id_split[0]}/{id_split[1]}/{id_split[2]}/{file_name}"

        s3 = boto3.resource("s3")
        obj = s3.Object(bucket_name, s3_path)
        joke = json.loads(obj.get()['Body'].read().decode('utf-8'))
        logger.info(f"joke: {joke}")

        return {
            "statusCode": 200,
            "body": joke.get("value")
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": str(e)
        }