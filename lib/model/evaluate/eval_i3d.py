"""
Transfer learning Kinetics i3d
https://github.com/deepmind/kinetics-i3d
"""
import argparse
import numpy as np
import sonnet as snt
import glob
from datetime import datetime
import tensorflow as tf

from lib.model.architectures import i3d
from lib.model.config import CONFIG
from lib.model.loaders.kinetics import KineticsLoader
from lib.model.evaluation import draw_cf_matrix

_BATCH_SIZE = 1
_LEARNING_RATE = 0.001
_EVAL_STEP_INTERVAL = 10

_SAMPLE_VIDEO_FRAMES = 150
_IMAGE_SIZE = 224
_NUM_CLASSES = CONFIG['num_relationships']

_DATA_DIR = 'data/kinetics'

_CHECKPOINT_PATH = 'data/weights/i3d_transfer/model'

tf.logging.set_verbosity(tf.logging.INFO)

parser = argparse.ArgumentParser()
args = parser.parse_args()


def load_data():
    vid_paths = glob.glob("{}/*.npy".format(_DATA_DIR))
    vid_paths.sort()
    dataset = tf.data.TFRecordDataset(vid_paths)

    return dataset


def main(unused_argv):
    # TODO: Train RGB and flow models separately

    rgb_input = tf.placeholder(
        tf.float32,
        shape=(_BATCH_SIZE, _SAMPLE_VIDEO_FRAMES, _IMAGE_SIZE, _IMAGE_SIZE, 3))
    rgb_y = tf.placeholder(tf.int64, [None, _NUM_CLASSES])

    with tf.variable_scope('RGB'):
        rgb_model = i3d.InceptionI3d(
            _NUM_CLASSES, spatial_squeeze=True, final_endpoint='Mixed_5c')
        rgb_net, _ = rgb_model(
            rgb_input, is_training=False, dropout_keep_prob=1.0)

        end_point = 'Logits'
        with tf.variable_scope(end_point):
            rgb_net = tf.nn.avg_pool3d(rgb_net, ksize=[1, 2, 7, 7, 1],
                                       strides=[1, 1, 1, 1, 1], padding=snt.VALID)

            logits = i3d.Unit3D(output_channels=_NUM_CLASSES,
                                kernel_shape=[1, 1, 1],
                                activation_fn=None,
                                use_batch_norm=False,
                                use_bias=True,
                                name='Conv3d_0c_1x1')(rgb_net, is_training=True)

            logits = tf.squeeze(logits, [2, 3], name='SpatialSqueeze')
            averaged_logits = tf.reduce_mean(logits, axis=1)

    rgb_variable_map = {}
    for variable in tf.global_variables():
        if variable.name.split('/')[0] == 'RGB':
            rgb_variable_map[variable.name.replace(':0', '')] = variable
    rgb_saver = tf.train.Saver(var_list=rgb_variable_map, reshape=True)

    model_predictions = tf.nn.softmax(averaged_logits)

    dataset = KineticsLoader(_BATCH_SIZE, _NUM_CLASSES, 'test')

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)

        print('Loading checkpoint from {}'.format(_CHECKPOINT_PATH))
        rgb_saver.restore(sess, _CHECKPOINT_PATH)

        y_true = []
        y_pred = []
        for i in range(len(dataset)):
            print('Step: {}'.format(i))
            batch_xs, batch_ys = dataset.next_batch()

            out_prediction = sess.run(model_predictions, feed_dict={rgb_input: batch_xs,
                                                           rgb_y: batch_ys})

            out_prediction = np.argmax(out_prediction[0])
            y_pred.append(out_prediction)
            y_true.append(np.argmax(batch_ys[0]))
            print('Predicted: {} | Truth: {}'.format(out_prediction, np.argmax(batch_ys[0])))

        draw_cf_matrix(y_true, y_pred)


if __name__ == '__main__':
    tf.app.run(main)
