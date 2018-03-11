import json
import time

import numpy as np
from lib.sort import Sort

THRESHOLD = 0.9


def load_bboxes(bboxes_file):
    """
    d[frame_no][bbox_no]

    [x1,y1,x2,y2,confidence]
    """
    with open(bboxes_file) as f:
        d = json.load(f)
        return d


def apply_tracker(bboxes_file):
    print('Running tracker')
    bboxes = load_bboxes(bboxes_file)

    tracker = Sort()

    bbox_annotations = []
    start = time.time()
    for frame in bboxes:
        f = frame['boxes']
        f[:] = [x for x in f if x[4] > THRESHOLD]
        trackers = tracker.update(np.array(f))

        # Cast to int
        trackers = trackers.astype(int)

        # Convert [x1,y1,x2,y2] to [x1,y1,w,h]
        trackers[:, 2:4] = trackers[:, 2:4] - trackers[:, 0:2]

        # Move Tracker ID to 1st column    
        trackers = trackers[:, [4, 0, 1, 2, 3]]

        trackers = trackers.tolist()

        bbox_annotations.append(trackers)

    total = time.time() - start

    print('Total time: {}s | Per frame: {}s'.format(total, total / len(bboxes)))

    return bbox_annotations
