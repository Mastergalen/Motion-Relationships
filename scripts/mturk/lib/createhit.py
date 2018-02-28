import random
from lib import apiclient

external_url = 'https://s3.amazonaws.com/amt-motion-relationships/hit.html'


def get_env_settings(is_production=False):
    if is_production:
        return {
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
            'max_assignments': 3,
            'reward': '0.20'
        }
    else:
        return {
            'qualification_requirements': [],
            'lifetime': 2629743, # 1 month
            'max_assignments': 50,
            'reward': '0.20'
        }



def create_hit_type(isProduction):
    settings = get_env_settings(isProduction)
    client = apiclient.create(isProduction)

    response = client.create_hit_type(
        AssignmentDurationInSeconds=1800, # 30 minutes
        AutoApprovalDelayInSeconds=86400, # 24 hours
        Reward=settings['reward'],
        Title='Annotate objects in a 5s video',
        Keywords='annotate, video',
        Description='Your task is to label the relationships between moving objects in a short 5s video, out of 4 choices. An experienced annotator can complete this in around 1 minute.',
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

def create_hit(video_id, hit_type_id, is_production=False):
    print("Creating HIT for {}".format(video_id))
    settings = get_env_settings(is_production)
    # In sandbox mode, allow duplicate HITs
    unique_token = video_id + str(random.randint(0, 10000))

    if is_production:
        unique_token = video_id

    client = apiclient.create(is_production)

    external_question = """
    <ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
    <ExternalURL>{}?video={}</ExternalURL>
    <FrameHeight>800</FrameHeight>
    </ExternalQuestion>
    """.format(external_url, video_id)

    response = client.create_hit_with_hit_type(
        HITTypeId=hit_type_id,
        MaxAssignments=settings['max_assignments'],
        LifetimeInSeconds=settings['lifetime'],
        Question=external_question,
        RequesterAnnotation="By Galen Han (galen.han.14@ucl.ac.uk) | Video ID: {}".format(video_id),
        UniqueRequestToken=unique_token,
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception(response)
