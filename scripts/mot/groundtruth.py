"""
Script for converting data from the MOT challenge into a .json format for the annotation UI tool
"""
import argparse
import configparser
import csv
import json

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, help='Path to video folder')

args = parser.parse_args()

config = configparser.ConfigParser()

config.read(args.path + '/seqinfo.ini')

with open(args.path + '/gt/gt.txt', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    arr = [[] for i in range(int(config['Sequence']['seqLength']))]

    # <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <x>, <y>, <z>
    count = 0

    for row in reader:
        frame = int(row[0])
        id = int(row[1])
        bb_left = int(row[2])
        bb_top = int(row[3])
        bb_width = int(row[4])
        bb_height = int(row[5])
        conf = int(row[6])

        if conf == 0:
            continue

        arr[frame - 1].append((id, bb_left, bb_top, bb_width, bb_height))
        count += 1

with open('output.json', 'w') as outfile:
    json.dump({
        'frameRate': int(config['Sequence']['frameRate']),
        'totalFrames': int(config['Sequence']['seqLength']),
        'width': int(config['Sequence']['imWidth']),
        'height': int(config['Sequence']['imHeight']),
        'annotations': arr
    }, outfile, indent=2)
