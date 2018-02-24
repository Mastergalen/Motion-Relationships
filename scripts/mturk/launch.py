"""
Submits the HIT as an External Question
"""
import argparse
import lib.createhit as createhit
from lib.utils.prompt import query_yes_no

parser = argparse.ArgumentParser()
parser.add_argument('--production', type=bool, help='Launch in production mode', default=False)
args = parser.parse_args()

videoIds = [
    '32CH8Op4VJw-419',
    'NuOiKCBO1hU-422',
    'Xbw_9hrp2KY-420',
    '05v8MA6SZ54-129',
    'G-ie5hQbG2s-412'
]

if args.production:
    res = query_yes_no("In PRODUCTION, proceed?", default="no")

    if not res:
        print('Aborting')
        exit(-1)

hitTypeId = createhit.create_hit_type(args.production)

print("Created HIT Type: {}".format(hitTypeId))

for vid in videoIds:
    createhit.create_hit(vid, hitTypeId, args.production)
