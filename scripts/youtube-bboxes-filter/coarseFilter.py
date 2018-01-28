"""
Filter the original YouTube BB dataset
"""
from pandas import DataFrame, read_csv
import pandas as pd
import numpy as np
from pdb import set_trace
# pd.options.display. = '{:.2f}'.format

df = pd.read_csv('youtube_boundingboxes_detection_train.csv',
                 header=None,
                 names=['youtube_id',
                        'timestamp_ms',
                        'class_id',
                        'class_name',
                        'object_id',
                        'object_presence',
                        'xmin',
                        'xmax',
                        'ymin',
                        'ymax'
                       ],
                 dtype={
                     'youtube_id': str,
                     'timestamp_ms': np.uint32,
                     'class_id': np.uint32,
                     'class_name': str,
                     'object_id': np.uint32,
                     'object_presence': str,
                     'xmin': np.float64,
                     'xmax': np.float64,
                     'ymin': np.float64,
                     'ymax': np.float64
                 },
                 delimiter=',')

# Class IDs:
# Person: 0
# Car: 23
g = df.groupby(['youtube_id'])

print("Total videos to process: {}".format(len(g)))

# Needs to have more than 1 type of class in the video
def filter_diversity(x):
    return len(x.groupby('class_name')) > 1

# Video contains car
def filter_contains_cars(x):
    return 23 in x['class_id'].unique()

def filter_undesired(x):
    undesired_class_ids = [6, 10, 11, 12, 14, 18, 20]
    intersection = len(np.intersect1d(x['class_id'].unique(), undesired_class_ids))

    return intersection == 0

print("Filter cars")
filtered = g.filter(filter_contains_cars).groupby('youtube_id')
print("Filter undesired classes")
filtered = filtered.filter(filter_undesired)

print("Total videos: {}".format(len(filtered.groupby('youtube_id'))))

print("Writing to csv")
filtered.to_csv('car.csv')

set_trace()
