import numpy as np
from lib.database.models import *


def inter_annotator_score(clip_id):
    res = VideoClip \
        .select() \
        .join(Assignment) \
        .join(Annotation) \
        .where(VideoClip.id == clip_id)

    video_clip = res.get()

    vid_dict = model_to_dict(video_clip, backrefs=True)

    all_ids = all_ids_in_clip(clip_id)
    assignment_count = len(vid_dict['assignment_set'])

    # Convert annotations into a matrix
    annotations = np.zeros((assignment_count, len(all_ids), len(all_ids)), dtype=np.uint8)
    for i, assignment in enumerate(vid_dict['assignment_set']):
        for annotation in assignment['annotation_set']:
            start_idx = all_ids.index(annotation['start'])
            end_idx = all_ids.index(annotation['end'])
            relationship_id = relationship_to_id[annotation['relationship']]
            annotations[i, start_idx, end_idx] = relationship_id

    M = agreement.collapse(annotations, len(relationship_to_id))
    kappa = agreement.fleiss_kappa(M)
    print("Video {} Kappa {}".format(clip_id, kappa))


def collapse(annotations, k):
    """
    Reformat annotation matrix into frequency of annotating by the same class

    :param annotations: (r, n, n)
        * r is the number of annotators
        * n is the number of entities
    :type annotations: ndarray
    :param k: Number of categories
    :type k: int
    :return: matrix of shape (:attr: `n`, :attr: `k`)
    """
    r, n, n = annotations.shape
    annotations = annotations.reshape((r, n * n))
    M = np.zeros((n * n, k), dtype=np.uint16)

    for i in range(n * n):
        unique, counts = np.unique(annotations[:, i], return_counts=True)
        for category_id, count in dict(zip(unique, counts)).items():
            M[i, category_id] = count

    return M


def fleiss_kappa(M):
    """
    Calculate Fleiss kappa

    :param M: matrix of shape (:attr: `n`, :attr: `k`)
    :return: kappa score from -1.0 (total disagreement) to 1.0 (total agreement)
    :rtype: float

    .. references: Fleiss, J. L. (1971).
        Measuring nominal scale agreement among many raters.
        Psychological bulletin, 76(5), 378.
    """
    n, k = M.shape  # N is # of subjects, k is # of categories
    n_raters = float(np.sum(M[0, :]))  # number of raters

    p = np.sum(M, axis=0) / (n * n_raters)
    P = (np.sum(M * M, axis=1) - n_raters) / (n_raters * (n_raters - 1))
    p_bar = np.sum(P) / n
    p_bar_e = np.sum(np.power(p, 2))

    kappa = (p_bar - p_bar_e) / (1 - p_bar_e)

    return kappa
