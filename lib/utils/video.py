import os
import cv2


def extract_frame(path, frame_no):
    cap = cv2.VideoCapture(path)

    cap.set(1, frame_no)
    ret, frame = cap.read()

    if not ret:
        raise Exception('Frame could not be read')

    return frame


def extract_frames(vidcap, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    digits = len(str(length))

    success, image = vidcap.read()

    count = 0
    while success:
        cv2.imwrite(
            "{}/frame_{number:0{width}d}.jpg".format(output_dir, number=count, width=digits),
            image
        )
        count += 1
        success, image = vidcap.read()
