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

    needs_review = []
    for clip in clips:
        clip_id = clip['video_clip_id']
        if clip['has_expert']:
            print('Using expert annotation for {}'.format(clip_id))
            save(clip_id, True)
            continue
        score = agreement.inter_annotator_score(clip_id)
        print(clip_id, score)

        if score > KAPPA_THRESHOLD:
            save(clip_id, False)
        else:
            needs_review.append(clip_id)

    print(needs_review)
    print("{}/{} clips need review".format(len(needs_review), len(clips)))


def save(clip_id, expert_only):
    print("Saving {}".format(clip_id))

    annotations = agreement.fetch_all_annotations(clip_id, expert_only)

    merged = agreement.merge_annotations(annotations)

    data.write('labels', '{}.json'.format(clip_id), merged.tolist())


if __name__ == '__main__':
    run()
    print('Finished export')
