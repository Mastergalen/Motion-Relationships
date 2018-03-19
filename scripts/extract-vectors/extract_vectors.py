import os
import glob
import json
import lib.preprocessing.extract_vectors as extract_vectors
from lib.utils.loader import load_bboxes

DATA_DIR = '../../data'

for path in glob.glob(os.path.join(DATA_DIR, 'clips/*.json')):
    clip_id = os.path.splitext(os.path.basename(path))[0]

    print("Processing clip {}".format(clip_id))

    output_path = os.path.join(DATA_DIR, 'flows', '{}.json'.format(clip_id))

    boxes = load_bboxes(path)
    flow_vectors = extract_vectors.in_clip(boxes)

    with open(output_path, 'w') as out:
        json.dump(flow_vectors.tolist(), out)
