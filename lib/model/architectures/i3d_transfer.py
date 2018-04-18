"""
Transfer learning Kinetics i3d
https://github.com/deepmind/kinetics-i3d
"""
import argparse
import sonnet as snt
from datetime import datetime
import tensorflow as tf

from lib.model.architectures import i3d
from lib.model.config import CONFIG
from lib.model.loaders.kinetics import KineticsLoader

_BATCH_SIZE = 1
_TRAINING_STEPS = 2000
_LEARNING_RATE = 0.001
_EVAL_STEP_INTERVAL = 10

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


def add_evaluation_step(result_tensor, ground_truth_tensor):
    """Inserts the operations we need to evaluate the accuracy of our results.
    Args:
      result_tensor: The new final node that produces results.
      ground_truth_tensor: The node we feed ground truth data
      into.
    Returns:
      Tuple of (evaluation step, prediction).
    """
    with tf.name_scope('accuracy'):
        with tf.name_scope('correct_prediction'):
            prediction = tf.argmax(result_tensor, 1)
            correct_prediction = tf.equal(prediction, ground_truth_tensor)
        with tf.name_scope('accuracy'):
            evaluation_step = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    tf.summary.scalar('accuracy', evaluation_step)
    return evaluation_step, prediction


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

            # TODO: Remove dropout during eval
            rgb_net = tf.nn.dropout(rgb_net, 0.7)

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
        if variable.name.split("/")[-4] == "Logits":
            continue
        if variable.name.split('/')[0] == 'RGB':
            rgb_variable_map[variable.name.replace(':0', '')] = variable
    rgb_saver = tf.train.Saver(var_list=rgb_variable_map, reshape=True)

    model_predictions = tf.nn.softmax(averaged_logits)
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model_predictions, labels=rgb_y))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=_LEARNING_RATE).minimize(loss)

    dataset = KineticsLoader(_BATCH_SIZE, _NUM_CLASSES, 'training')

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)

        run_opts = tf.RunOptions(report_tensor_allocations_upon_oom = True)

        print('Restoring weights...')
        rgb_saver.restore(sess, _CHECKPOINT_PATHS['rgb'])

        evaluation_step, _ = add_evaluation_step(model_predictions, rgb_y)

        train_saver = tf.train.Saver()

        for i in range(_TRAINING_STEPS):
            print('Step: {}'.format(i))
            batch_xs, batch_ys = dataset.next_batch()
            sess.run(optimizer, feed_dict={rgb_input: batch_xs, rgb_y: batch_ys}, options=run_opts)

            is_last_step = (i + 1 == _TRAINING_STEPS)
            if (i % _EVAL_STEP_INTERVAL) == 0 or is_last_step:
                train_accuracy, cross_entropy_value = sess.run(
                    [evaluation_step, loss],
                    feed_dict={rgb_input: batch_xs,
                               rgb_y: batch_ys})
                tf.logging.info('%s: Step %d: Train accuracy = %.1f%%' %
                                (datetime.now(), i, train_accuracy * 100))
                tf.logging.info('%s: Step %d: Cross entropy = %f' %
                                (datetime.now(), i, cross_entropy_value))
                # TODO: Use validation set

        train_saver.save(sess, 'data/weights/i3d_transfer/model')


if __name__ == '__main__':
    tf.app.run(main)
