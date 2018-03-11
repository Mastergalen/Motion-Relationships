"""
Submits the HIT as an External Question
"""
import argparse

import lib.mturk.createhit as create_hit
from lib.utils.prompt import query_yes_no

parser = argparse.ArgumentParser()
parser.add_argument('--production', action='store_true', help='Launch in production mode')
args = parser.parse_args()

VIDEO_IDS = [
    'Xbw_9hrp2KY-420'
]

if args.production:
    SETTINGS = create_hit.get_env_settings(args.production)
    TOTAL_ASSIGNMENTS = SETTINGS['max_assignments'] * len(VIDEO_IDS)
    print("About to launch {} videos".format(len(VIDEO_IDS)))
    print("{} assignments per video".format(SETTINGS['max_assignments']))
    print("{} Total assigmnents".format(TOTAL_ASSIGNMENTS))
    TOTAL_COST = float(SETTINGS['reward']) * TOTAL_ASSIGNMENTS
    print("Total cost: {0:.2f}".format(TOTAL_COST))
    res = query_yes_no("In PRODUCTION, proceed?", default="no")

    if not res:
        print('Aborting')
        exit(-1)

hit_type_id = createhit.create_hit_type(args.production)

print("Created HIT Type: {}".format(hit_type_id))

for vid in VIDEO_IDS:
    createhit.create_hit(vid, hit_type_id, args.production)
