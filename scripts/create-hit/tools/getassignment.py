import argparse
import pprint
from lib import apiclient

parser = argparse.ArgumentParser()
parser.add_argument('assignmentid', type=str, help='HIT ID')
args = parser.parse_args()

ENDPOINT = 'https://mturk-requester.us-east-1.amazonaws.com'

client = apiclient.create(ENDPOINT)

print("Fetching assignment {}".format(args.assignmentid))

response = client.get_assignment(AssignmentId=args.assignmentid)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(response)
