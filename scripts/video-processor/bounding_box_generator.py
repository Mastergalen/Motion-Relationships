"""
Generate bounding boxes using Detectron
"""
import cv2
import os
import shutil

directory = 'downloads'
tmpDirectory = 'tmp'

def generate_images(filepath):
    vidcap = cv2.VideoCapture(filepath)

    success,image = vidcap.read()

    count = 0
    while success:
        cv2.imwrite(tmpDirectory + "/frame_%d.jpg" % count, image)     # save frame as JPEG file
        if cv2.waitKey(10) == 27:                     # exit if Escape is hit
            break
        count += 1
        success,image = vidcap.read()

def identify_bounding_boxes():
    # TODO
    pass

for filename in os.listdir(directory):
    if filename.endswith(".mp4"): 
        print("Processing {}".format(filename))
        filepath = os.path.join(directory, filename)

        if not os.path.exists(tmpDirectory):
            os.makedirs(tmpDirectory)

        generate_images(filepath)

        identify_bounding_boxes()

        shutil.rmtree(tmpDirectory) 
    
    else:
        continue

    # TODO Remove break
    break