import boto3
import os
import random
from dotenv import load_dotenv

region_name = 'us-east-1'
external_url = 'https://s3.amazonaws.com/amt-motion-relationships/hit.html'

load_dotenv('../../.env', verbose=True)

def get_env_settings(isProduction):
    if isProduction:
        return {
            'endpoint_url': 'https://mturk-requester.us-east-1.amazonaws.com',
            'qualification_requirements': [
                {
                    'QualificationTypeId': '2F1QJWKUDD8XADTFD2Q0G6UTO95ALH',
                    'Comparator': 'Exists',
                    'RequiredToPreview': False
                },
            ],
            'lifetime': 259200, # 3 days,
            'max_assignments': 3
        }
    else:
        return {
            'endpoint_url': 'https://mturk-requester-sandbox.us-east-1.amazonaws.com',
            'qualification_requirements': [],
            'lifetime': 2629743, # 1 month
            'max_assignments': 50
        }

def create_client(endpoint_url):
    return boto3.client(
        'mturk',
        endpoint_url=endpoint_url,
        region_name=region_name,
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
    )

def create_hit_type(isProduction):
    settings = get_env_settings(isProduction)
    client = create_client(settings['endpoint_url'])

    response = client.create_hit_type(
        AssignmentDurationInSeconds=10800, # 3 hours  
        AutoApprovalDelayInSeconds=86400, # 24 hours
        Reward='0.20',
        Title='Annotate objects in a 5s video',
        Keywords='annotate, video',
        Description='Your task is to label the relationships between moving objects in a short 5s video, out of 5 choices.',
        QualificationRequirements=settings['qualification_requirements']
    )

     # Set notification settings
    res = client.update_notification_settings(
        HITTypeId=response['HITTypeId'],
        Notification={
            'Destination': 'arn:aws:sns:us-east-1:506356021079:mturk-motion-relationship-assignment-submitted',
            'Transport':'SNS',
            'Version': '2006-05-05',
            'EventTypes': [
                'AssignmentSubmitted',
            ]
        },
        Active=True
    )
    print(res)

    return response['HITTypeId']

def create_hit(videoId, hitTypeId, isProduction=False):
    print("Creating HIT for {}".format(videoId))
    settings = get_env_settings(isProduction)    
    # In sandbox mode, allow duplicate HITs
    unique_token = videoId + str(random.randint(0,10000))

    if isProduction:
        unique_token = videoId
        
    client = create_client(settings['endpoint_url'])

    external_question = """
    <ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
    <ExternalURL>{}?video={}</ExternalURL>
    <FrameHeight>800</FrameHeight>
    </ExternalQuestion>
    """.format(external_url, videoId)

    response = client.create_hit_with_hit_type(
        HITTypeId=hitTypeId,
        MaxAssignments=settings['max_assignments'],
        LifetimeInSeconds=settings['lifetime'],
        Question=external_question,
        RequesterAnnotation="By Galen Han (galen.han.14@ucl.ac.uk) | Video ID: {}".format(videoId),
        UniqueRequestToken=unique_token,
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception(response)
