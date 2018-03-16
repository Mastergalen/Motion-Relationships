import os
import json


def load_bboxes(clip_id):
    """
    Load the bounding boxes from .json file
    :param clip_id:
    :return: Dictionary
        key is the Entity ID
        val is a 2 tuple: (frame_no, list of bboxes for each frame)
    :rtype: dict
    """
    path = os.path.join('test-videos', '{}.json'.format(clip_id))

    bbox_dict = {}
    with open(path) as f:
        data = json.load(f)

    for t, frame in enumerate(data['annotations']):
        for entity in frame:
            entity_id = entity[0]
            box_list = bbox_dict.get(entity_id)
            if box_list is None:
                box_list = []
            box_list.append((t, entity[1:5]))
            bbox_dict[entity_id] = box_list

    return bbox_dict
