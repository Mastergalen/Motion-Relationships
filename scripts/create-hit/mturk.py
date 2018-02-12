import boto3
import os
import random
from dotenv import load_dotenv

region_name = 'us-east-1'
external_url = 'https://s3.amazonaws.com/amt-motion-relationships/hit.html'

load_dotenv('../../.env', verbose=True)

def create_client(endpoint_url):
    return boto3.client(
        'mturk',
        endpoint_url=endpoint_url,
        region_name=region_name,
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
    )

def create_hit(videoId, isProduction):
    print("Creating HIT for {}".format(videoId))

    endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
    master_qualification_id = '2ARFPLSP75KLA8M8DH1HTEQVJT3SY6'
    qualification_requirements = []
    # In sandbox mode, allow duplicate HITs
    unique_token = videoId + str(random.randint(0,10000))

    if isProduction:
        endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'
        master_qualification_id = '2F1QJWKUDD8XADTFD2Q0G6UTO95ALH'
        qualification_requirements = [
            {
                'QualificationTypeId': master_qualification_id,
                'Comparator': 'Exists',
                'RequiredToPreview': False
            },
        ]
        unique_token = videoId
        
    client = create_client(endpoint_url)

    external_question = """
    <ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
    <ExternalURL>{}?video={}</ExternalURL>
    <FrameHeight>800</FrameHeight>
    </ExternalQuestion>
    """.format(external_url, videoId)

    response = client.create_hit(
        MaxAssignments=3,
        AutoApprovalDelayInSeconds=86400, # 24 hours
        LifetimeInSeconds=259200, # 3 days
        AssignmentDurationInSeconds=10800, # 3 hours  
        Reward='0.17',
        Title='Annotate objects in a 5s video',
        Keywords='annotate, video',
        Description='Your task is to label the relationships between moving objects in a short 5s video, out of 5 choices.',
        Question=external_question,
        RequesterAnnotation="By Galen Han (galen.han.14@ucl.ac.uk) | Video ID: {}".format(videoId),
        QualificationRequirements=qualification_requirements,
        UniqueRequestToken=unique_token,
    )

    print(response)
