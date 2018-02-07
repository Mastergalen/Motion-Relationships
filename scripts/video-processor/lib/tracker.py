import numpy as np
import json
import time
from sort import Sort

from pdb import set_trace


def load_bboxes():
    """
    d[frame_no][bbox_no]

    [x1,y1,x2,y2,confidence]
    """
    with open('bboxes.json') as f:
        d = json.load(f)

        return d

bboxes = load_bboxes()

tracker = Sort()

bbox_annotations = []
start = time.time()
for frame in bboxes:
    trackers = tracker.update(np.array(frame))

    # Cast to int
    trackers = trackers.astype(int)

    # Convert [x1,y1,x2,y2] to [x1,y1,w,h]
    trackers[:, 2:4] = trackers[:, 2:4] - trackers[:, 0:2]

    # Move Tracker ID to 1st column    
    trackers = trackers[:,[4,0,1,2,3]]

    trackers = trackers.tolist()

    bbox_annotations.append(trackers)

total = time.time() - start

print('Total time: {}s | Per frame: {}s'.format(total, total / len(bboxes)))

with open('output.json', 'w') as out:
    json.dump({
        'frameRate': 29.97, # TODO Remove fixed
        'totalFrames': 149,
        'width': 1280,
        'height': 720,
        'annotations': bbox_annotations
    }, out, indent=4)
