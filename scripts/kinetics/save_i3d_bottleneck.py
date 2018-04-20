"""
Save bottleneck features of kinetics-i3d
https://github.com/deepmind/kinetics-i3d

Need to run scripts/kinetics/video_preprocess.py first to crop videos into
correct size
"""
import argparse
import numpy as np
import os
import glob
import progressbar
import tensorflow as tf

from lib.model.architectures import i3d
from lib.model.config import CONFIG
from lib.model.loaders.kinetics import KineticsLoader

_BATCH_SIZE = 1

_SAMPLE_VIDEO_FRAMES = 150
_IMAGE_SIZE = 224
_NUM_CLASSES = CONFIG['num_relationships']

_DATA_DIR = 'data/kinetics'

_CHECKPOINT_PATHS = {
    'rgb': 'data/weights/kinetics-i3d/rgb_scratch/model.ckpt',
    'flow': 'data/weights/kinetics-i3d/flow_scratch/model.ckpt',
    'rgb_imagenet': 'data/weights/kinetics-i3d/rgb_imagenet/model.ckpt',
    'flow_imagenet': 'data/weights/kinetics-i3d/flow_imagenet/model.ckpt',
}

tf.logging.set_verbosity(tf.logging.INFO)

parser = argparse.ArgumentParser()
args = parser.parse_args()


def main(unused_argv):
    # TODO: Train RGB and flow models separately

    rgb_input = tf.placeholder(
        tf.float32,
        shape=(_BATCH_SIZE, _SAMPLE_VIDEO_FRAMES, _IMAGE_SIZE, _IMAGE_SIZE, 3))
    rgb_y = tf.placeholder(tf.int64, [None, _NUM_CLASSES])

    with tf.variable_scope('RGB'):
        rgb_model = i3d.InceptionI3d(
            _NUM_CLASSES, spatial_squeeze=True, final_endpoint='Mixed_5c')
        rgb_bottleneck, _ = rgb_model(
            rgb_input, is_training=False, dropout_keep_prob=1.0)

    rgb_variable_map = {}
    for variable in tf.global_variables():
        if variable.name.split('/')[0] == 'RGB':
            rgb_variable_map[variable.name.replace(':0', '')] = variable
    rgb_saver = tf.train.Saver(var_list=rgb_variable_map, reshape=True)

    dataset = KineticsLoader(_BATCH_SIZE, _NUM_CLASSES, 'training')

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)

        print('Restoring weights...')
        rgb_saver.restore(sess, _CHECKPOINT_PATHS['rgb'])

        video_data_paths = glob.glob(os.path.join(_DATA_DIR, 'rgb_*.npy'))
        assert len(video_data_paths) > 0

        bar = progressbar.ProgressBar()
        for path in bar(video_data_paths):
            clip_id = '_'.join(os.path.splitext(os.path.basename(path))[0].split('_')[1:])
            x = np.zeros((1, _SAMPLE_VIDEO_FRAMES, _IMAGE_SIZE, _IMAGE_SIZE, 3))
            x[0, ...] = np.load(path)
            out_bottleneck = sess.run(rgb_bottleneck, feed_dict={rgb_input: x})

            np.save('data/kinetics_bottleneck/{}.npy'.format(clip_id), out_bottleneck)


if __name__ == '__main__':
    tf.app.run(main)
