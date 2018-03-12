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
    '4WZImk31njQ-196',
    'nt3D26lrkho-413',
    'HIuqmNiKJx4-412',
    'NuOiKCBO1hU-423',
    'NuOiKCBO1hU-424',
    'Q-utfnQmJMc-201',
    'Y6Asp_FtgRA-424',
    '_x8FdEXh_Tg-426',
    'Aqko6DwEqq4-352',
    '5thMEw1tRC0-239',
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

hit_type_id = create_hit.create_hit_type(args.production)

print("Created HIT Type: {}".format(hit_type_id))

for vid in VIDEO_IDS:
    create_hit.create_hit(vid, hit_type_id, args.production)
