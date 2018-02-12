"""
Submits the HIT as an External Question
"""
import mturk
from utils.prompt import query_yes_no

isProduction = False
videoIds = [
    '-3K26M-m_00'
]

if isProduction:
    res = query_yes_no("In PRODUCTION, proceed?", default="no")
    
    if not res:
        print('Aborting')
        exit(-1)

hitTypeId = mturk.create_hit_type(isProduction)

print("Created HIT Type: {}".format(hitTypeId))

for vid in videoIds:
    mturk.create_hit(vid, hitTypeId, isProduction)
