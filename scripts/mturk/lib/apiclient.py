"""
MTurk client
"""
import os
import boto3
import pdb
from dotenv import load_dotenv

REGION = 'us-east-1'

load_dotenv('../../.env', verbose=True)

def create(endpoint_url):
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret = os.environ.get('AWS_SECRET_KEY')

    if access_key is None or secret is None:
        raise ValueError('AWS keys not set!')

    return boto3.client(
        'mturk',
        endpoint_url=endpoint_url,
        region_name=REGION,
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
    )
