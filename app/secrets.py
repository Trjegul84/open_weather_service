import json
import logging

import boto3
from botocore.exceptions import ClientError

from app.settings import Settings


logger = logging.getLogger(__name__)

settings = Settings()

def get_secret(secret_name):
    secret_name = secret_name
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY,
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    except ClientError as err:
        error_code = err.response['Error']['Code']
        match error_code:
            case "InternalServiceError":
                logger.error("An error occurred on the server side.")
            case "InvalidParameterException":
                logger.error("The parameter name or value is invalid.")
            case "InvalidRequestException":
                logger.error("A parameter value is not valid for the current state of the resource. Multiple causes to consider.")
            case "ResourceNotFoundException":
                logger.error("Secrets Manager can't find the resource that you asked for.")
            case _:
                raise err
        raise err

    secret = get_secret_value_response['SecretString']
    secret =json.loads(secret)

    for _, value in secret.items():
        secret_value = value

    return secret_value
