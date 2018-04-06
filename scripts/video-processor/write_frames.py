"""
Script for debugging purposes

Extracts frames to folder
"""
import argparse
import os

import cv2

from lib.utils.video import extract_frames

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('clip_id', type=str)
    args = parser.parse_args()

    print('Extracting frames for {}'.format(args.clip_id))

    vid_path = os.path.join('data/clips/{}.mp4'.format(args.clip_id))

    vidcap = cv2.VideoCapture(vid_path)
    extract_frames(vidcap, 'tmp')
