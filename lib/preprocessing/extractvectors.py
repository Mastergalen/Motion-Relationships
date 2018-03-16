import lib.utils.loader as loader


def extract_vectors(clip_id):
    bboxes = loader.load_bboxes(clip_id)
    pass


def interpolate_bboxes(start, end, length):
    """
    Linearly interpolates starting position
    :param start:
    :param end:
    :param length: Number of new frames to interpolate
    :return:
    """
    pass