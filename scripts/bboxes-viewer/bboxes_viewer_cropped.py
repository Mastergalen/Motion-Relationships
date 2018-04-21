"""
Visualise bounding boxes in a cropped Kinetics clip
"""
import argparse
import os
import progressbar
import warnings
import cv2
import numpy as np

from lib.utils import loader, video

_NB_FRAMES = 150
_CLIPS_DIR = os.path.join('data', 'clips')
_KINETICS_DIR = os.path.join('data', 'kinetics')
_OUT_DIR = 'tmp/vis-bboxes'

parser = argparse.ArgumentParser()
parser.add_argument('clip_id', type=str)
parser.add_argument('--entity_ids', type=int, nargs='+', help='Draw only bboxes matching IDs')
args = parser.parse_args()

_RESIZE_SIZE = 256
_CROP_SIZE = 224


def __convert_vector__(boxes, scale_factor, translation):
    for i, b in enumerate(boxes):
        boxes[i] = (b[0], np.round((b[1] * scale_factor) - translation).astype(np.int32))
    return boxes


def main():
    json_path = os.path.join(_CLIPS_DIR, '{}.json'.format(args.clip_id))
    video_path = os.path.join(_KINETICS_DIR, 'rgb_{}.mp4'.format(args.clip_id))
    bboxes = loader.load_bboxes(json_path, max_frames=_NB_FRAMES)

    h, w = loader.get_video_dims(json_path)
    smallest_dim = min(h, w)
    max_dim = max(h, w)

    scale_factor = _RESIZE_SIZE / smallest_dim
    translation = np.array([
        ((max_dim * scale_factor) - _CROP_SIZE) // 2,
        (_RESIZE_SIZE - _CROP_SIZE) // 2,
        0,  # No need to translate w and h vector again
        0
    ])

    if not os.path.exists(_OUT_DIR):
        os.makedirs(_OUT_DIR)

    cap = cv2.VideoCapture(video_path)

    annotation_map = {}

    for entity_id, entity_bbox in enumerate(bboxes):
        converted = __convert_vector__(entity_bbox, scale_factor, translation)
        for t, bbox_coords in converted:
            if t not in annotation_map:
                annotation_map[t] = {}
            annotation_map[t][entity_id] = bbox_coords

    bar = progressbar.ProgressBar()
    for t in bar(range(_NB_FRAMES)):
        if t in annotation_map:
            bboxes = annotation_map[t]
        else:
            bboxes = []

        try:
            frame = video.extract_frame(video_path, t, cv2_cap=cap)
        except:
            warnings.warn('Failed to read frame {}'.format(t))
            continue

        if args.entity_ids is None:
            entity_ids = bboxes.keys()
        else:
            entity_ids = args.entity_ids

        for entity_id in entity_ids:
            if entity_id not in bboxes:
                continue
            x, y, w, h = bboxes[entity_id]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

            if args.entity_ids is None:
                cv2.putText(frame, '{}'.format(entity_id), (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            color=(0, 255, 0),
                            thickness=2,
                            lineType=cv2.LINE_AA)

        cv2.imwrite(os.path.join(_OUT_DIR, '{:04d}.jpg'.format(t)), frame)


if __name__ == '__main__':
    main()
