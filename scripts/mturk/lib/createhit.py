import random
from lib import apiclient

external_url = 'https://s3.amazonaws.com/amt-motion-relationships/hit.html'


def get_env_settings(isProduction):
    if isProduction:
        return {
            'endpoint_url': 'https://mturk-requester.us-east-1.amazonaws.com',
            # TODO: Temporarily disable master's requirement
            # 'qualification_requirements': [
            #     {
            #         'QualificationTypeId': '2F1QJWKUDD8XADTFD2Q0G6UTO95ALH',
            #         'Comparator': 'Exists',
            #         'RequiredToPreview': False
            #     },
            # ],
            'qualification_requirements': [ ],
            'lifetime': 259200, # 3 days,
            'max_assignments': 1
        }
    else:
        return {
            'endpoint_url': 'https://mturk-requester-sandbox.us-east-1.amazonaws.com',
            'qualification_requirements': [],
            'lifetime': 2629743, # 1 month
            'max_assignments': 50
        }



def create_hit_type(isProduction):
    settings = get_env_settings(isProduction)
    client = apiclient.create(settings['endpoint_url'])

    response = client.create_hit_type(
        AssignmentDurationInSeconds=1800, # 30 minutes
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
    unique_token = videoId + str(random.randint(0, 10000))

    if isProduction:
        unique_token = videoId

    client = apiclient.create(settings['endpoint_url'])

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
