"""
Extracts only the video IDs
"""
import pandas as pd
import numpy as np
from pdb import set_trace
# pd.options.display. = '{:.2f}'.format

df = pd.read_csv('videos_with_cars.csv',
                 header=0,
                 names=['row_id',
                        'youtube_id',
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
                     'row_id': np.uint32,
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
# 0: Person
# 1: Bird
# 2: Bicycle
# 3: Boat
# 4: Bus
# 5: Bear
# 6: Cow
# 7: Cat
# 8: Giraffe
# 9: Potted plant
# 10: Horse
# 11: Motorcycle
# 12: Knife
# 13: Airplane
# 14: Skateboard
# 15: Train
# 16: Truck
# 17: Zebra
# 18: Toilet
# 19: Dog
# 20: Elephant
# 21: Umbrella
# 22: N/A
# 23: Car

g = df.groupby('youtube_id')

print("Found {} videos".format(len(g)))

# Write single video
g.first().to_csv('videos_with_cars_2.csv')
