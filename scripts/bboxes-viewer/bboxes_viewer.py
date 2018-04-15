import argparse
import os
import matplotlib.pyplot as plt

from lib.utils import loader

_NB_FRAMES = 150

parser = argparse.ArgumentParser()
parser.add_argument('clip_id', type=str)
parser.add_argument('entity_ids', type=int, nargs='+')
args = parser.parse_args()


def main():
    json_path = os.path.join('data', 'clips', '{}.json'.format(args.clip_id))
    bboxes = loader.load_bboxes(json_path, max_frames=_NB_FRAMES)

    for t in range(_NB_FRAMES):
        plt.imshow()


if __name__ == '__main__':
    main()
