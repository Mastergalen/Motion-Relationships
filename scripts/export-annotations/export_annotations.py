"""
Exports the annotations made by Mechanical Turk into ground truth format

Majority voting is used to resolve conflicts

Labels are stored in data/labels
"""
import lib.mturk.agreement as agreement
from lib.database.models import *
from lib.utils.datamanager import DataManager

KAPPA_THRESHOLD = 0.7
data = DataManager()


def run():
    clips = list(Assignment.approved().dicts())

    for clip in clips:
        clip_id = clip['video_clip_id']
        score = agreement.inter_annotator_score(clip_id)
        print(clip_id, score)

        if score > KAPPA_THRESHOLD:
            save(clip_id)


def save(clip_id):
    print("Saving {}".format(clip_id))
    annotations = agreement.fetch_all_annotations(clip_id)

    merged = agreement.merge_annotations(annotations)

    data.write('labels', '{}.json'.format(clip_id), merged.tolist())


if __name__ == '__main__':
    run()
    print('Finished export')
