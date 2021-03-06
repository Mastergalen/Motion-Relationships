import glob
import os
import  warnings

from lib.model.config import CONFIG


def list_labels(set):
    """
    :param set: 'test' or 'training'
    :return:
    """
    return list_files(os.path.join('labels', set))


def list_files(dir_name):
    dir_path = os.path.join(CONFIG['data_dir'], dir_name)
    pattern = os.path.join(dir_path, '*.json')
    files = glob.glob(pattern)
    files.sort()

    if len(files) == 0:
        warnings.warn('No files found matching {}'.format(pattern))

    return files
