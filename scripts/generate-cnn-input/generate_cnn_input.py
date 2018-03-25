import os
import json

import numpy as np
import cv2

from lib.model.loaders.helpers import list_labels
from lib.model.mask import generate_mask
from lib.utils.loader import load_bboxes
from lib.utils.video import extract_frame
from lib.model.config import CONFIG

OUTPUT_DIR = os.path.join('data', 'cnn_input')
CLIP_DIR = os.path.join('data', 'clips')
np.random.seed(12)


def generate_img(clip_id, id_pair):
    """
    Generate input image for entity pair `a` and `b`

    :param clip_id:
    :param id_pair: (a,b)
    :return: Frame no
    :rtype: int
    """
    id_A, id_B = id_pair
    box_path = os.path.join(CLIP_DIR, '{}.json'.format(clip_id))
    video_path = os.path.join(CLIP_DIR, '{}.mp4'.format(clip_id))
    boxes = load_bboxes(box_path)
    frame_no = find_common_frame(boxes[id_A], boxes[id_B])

    if frame_no is None:
        return None, None

    frame = extract_frame(video_path, frame_no)

    height, width, _ = frame.shape

    box_A = find_box_coords(boxes[id_A], frame_no)
    box_B = find_box_coords(boxes[id_B], frame_no)

    mask_A = generate_mask(box_A, (height, width))
    mask_B = generate_mask(box_B, (height, width))

    output_img = np.zeros((height, width, 3), dtype=np.uint8)

    output_img[:, :, 0] = mask_A
    # Only use green channel
    output_img[:, :, 1] = frame[:, :, 1]
    output_img[:, :, 2] = mask_B

    return output_img, frame_no


def find_common_frame(frames_A, frames_B):
    """
    Find frame in `clip_id` where both objects are present at the same time
    :return:
    """
    # Naively loop each frame and find intersection
    ids_A = extract_frame_ids(frames_A)
    ids_B = extract_frame_ids(frames_B)

    common_frames = np.intersect1d(ids_A, ids_B)

    # If no common frames could be found
    if common_frames.size == 0:
        return None

    return np.random.choice(common_frames)


def find_box_coords(bboxes, t):
    for b in bboxes:
        if b[0] == t:
            return b[1]


def extract_frame_ids(bboxes):
    ids = []
    for i in bboxes:
        ids.append(i[0])

    return ids


def create_dirs():
    for i in range(CONFIG['num_relationships']):
        dir_path = os.path.join(OUTPUT_DIR, str(i))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)


if __name__ == '__main__':
    print("Generating CNN input images")
    create_dirs()
    label_paths = list_labels()

    for path in label_paths:
        print(path)
        clip_id = os.path.splitext(os.path.basename(path))[0]

        labels = np.array(json.load(open(path)))

        for idx, label in np.ndenumerate(labels):
            # Skip relationships to itself
            if idx[0] == idx[1]:
                continue
            output_img, frame_no = generate_img(clip_id, idx)

            if output_img is None:
                continue

            output_path = os.path.join(
                OUTPUT_DIR,
                str(label),
                '{}-t{}-{}-{}.jpg'.format(clip_id, frame_no, str(idx[0]), str(idx[1]))
            )
            cv2.imwrite(output_path, output_img)
