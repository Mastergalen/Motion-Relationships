from collections import Counter


def get_class_weights(y):
    """
    Determine class weights based on frequency distribution of labels
    :param y:
    :return:
    """
    counter = Counter(y)
    majority = max(counter.values())
    return {cls: float(majority/count) for cls, count in counter.items()}