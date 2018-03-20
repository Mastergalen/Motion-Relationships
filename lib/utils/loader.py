import json
import numpy as np


def load_bboxes(path, max_frames=150):
    """
    Load the bounding boxes from .json file
    :param path: Path to .json file
    :param max_frames: Clip number of frames
    :return: List
        2D array
        1st level = entity
        2nd level = list of 2 tuples: (frame_no, list of bboxes for each frame)
    :rtype: list
    """

    bbox_dict = {}
    with open(path) as f:
        data = json.load(f)

    for t, frame in enumerate(data['annotations']):
        if t == max_frames:
            break
        for entity in frame:
            entity_id = entity[0]
            box_list = bbox_dict.get(entity_id)
            if box_list is None:
                box_list = []
            box_list.append((t, np.array(entity[1:5])))
            bbox_dict[entity_id] = box_list

    # Sort dictionary values by key
    bboxes = [val for key, val in sorted(bbox_dict.items(), reverse=True)]

    bboxes = interpolate_missing_frames(bboxes)

    return bboxes


def interpolate_missing_frames(bboxes):
    """
    Tracker may lose tracking suddenly, interpolate the missing frames linearly
    """
    for entity_idx, entity in enumerate(bboxes):
        if entity_idx != 2:
            continue
        prev_frame = None
        prev_val = None

        for t, val in entity:
            if (prev_frame is not None) and (t-1 != prev_frame):
                steps = t - prev_frame
                diff = (val - prev_val) / steps

                for i in range(steps - 1):
                    interp = np.round(prev_val + (i+1) * diff)
                    entity.append((prev_frame + i + 1, interp))

                entity.sort(key=lambda x: x[0])
                prev_frame += 1
            else:
                prev_frame = t
            prev_val = val

    return bboxes
