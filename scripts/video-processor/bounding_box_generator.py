"""
Generate bounding boxes using Detectron
"""
import cv2
import glob
import json
import logging
import os
import shutil
import subprocess
import time
from pathlib import Path
from lib.tracker import apply_tracker
from pdb import set_trace

directory = 'downloads'
tmpDirectory = 'tmp'

def generate_images(vidcap):
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    digits = len(str(length))

    success,image = vidcap.read()

    count = 0
    while success:
        cv2.imwrite(
            "{}/frame_{number:0{width}d}.jpg".format(tmpDirectory, number=count, width=digits),
            image
        )
        count += 1
        success,image = vidcap.read()

def generate_bounding_boxes():
    """
    Takes .jpg frames of video in ./tmp folder and applies bounding box detections.
    Results are written to './tmp/bboxes.json'
    """
    print('Applying detectron')
    detectron_dir = os.path.join(str(Path.home()), 'my-detectron')
    subprocess.run([
        "python2", os.path.join(detectron_dir, "tools/infer_simple.py"),
        "--cfg",
        os.path.join(
            detectron_dir,
            "configs/12_2017_baselines/e2e_mask_rcnn_X-101-32x8d-FPN_1x.yaml"
        ),
        "--output-dir", "tmp",
        "--image-ext", "jpg",
        "--wts",
        "https://s3-us-west-2.amazonaws.com/detectron/36761843/12_2017_baselines/e2e_mask_rcnn_X-101-32x8d-FPN_1x.yaml.06_35_59.RZotkLKI/output/train/coco_2014_train%3Acoco_2014_valminusminival/generalized_rcnn/model_final.pkl",
        "tmp"
    ], check=True, stdout=subprocess.DEVNULL)

vid_list = glob.glob("{}/*.mp4".format(directory))
total_videos = len(vid_list)

for i, file_path in enumerate(vid_list):
    start = time.time()
    file_name = os.path.basename(file_path)
    youtube_id = file_name.split('.')[0]
    annotation_path = os.path.join(directory, "{}.json".format(youtube_id))
    if os.path.isfile(annotation_path):
        print('Already processed {}, skipping'.format(youtube_id))
        continue
    else:
        print("Processing {} | {}/{}".format(file_name, i, total_videos))
    
    if not os.path.exists(tmpDirectory):
        os.makedirs(tmpDirectory)

    vidcap = cv2.VideoCapture(file_path)

    # Writes image frames in ./tmp
    generate_images(vidcap)

    # Takes image frames in ./tmp and writes a bounding box file ./tmp/bbox.json
    generate_bounding_boxes()

    # Apply tracker
    tracker_annotations = apply_tracker('./tmp/boxes.json')

    with open(annotation_path, 'w') as out:
        json.dump({
            'frameRate': vidcap.get(cv2.CAP_PROP_FPS),
            'totalFrames': 149,
            'width': int(vidcap.get(3)),
            'height': int(vidcap.get(4)),
            'annotations': tracker_annotations
        }, out, indent=4)

    shutil.rmtree(tmpDirectory)

    total = time.time() - start

    print('Finished processing {}. Time: {}'.format(youtube_id, total))
