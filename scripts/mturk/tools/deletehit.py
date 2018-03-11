import argparse
import pprint

from lib import apiclient

parser = argparse.ArgumentParser()
parser.add_argument('hitid', type=str, help='HIT ID')
args = parser.parse_args()

ENDPOINT = 'https://mturk-requester.us-east-1.amazonaws.com'

client = apiclient.create(ENDPOINT)

print("Fetching HIT {}".format(args.hitid))

response = client.delete_hit(HITId=args.hitid)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(response)
