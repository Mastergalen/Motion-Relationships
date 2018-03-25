import numpy as np


def in_clip(bboxes, max_frames=150):
    """
    Calculate all flow vectors for each entity in clip
    :param bboxes: Bounding Boxes
    :param max_frames:
    :return: flow sequence for entity
        Shape: [entity_idx, frame_idx, flow_vector]
        flow_vector: [x, y, v_x, v_y, a_x, a_y]
    :rtype: ndarray
    """
    entity_count = len(bboxes)

    flow = np.zeros((entity_count, max_frames, 6))
    for entity_idx, entity in enumerate(bboxes):
        counter = 0
        for t, val in entity:
            # Calculate box center
            # FIXME: Bug: Calculate center given (x1, y1, width, height)
            x = np.average(val[0:4:2])
            y = np.average(val[1:4:2])

            v_x = v_y = a_x = a_y = np.NaN

            if counter > 0:
                f_prev = flow[entity_idx, t-1, :]
                v_x, v_y = np.array([x, y]) - f_prev[0:2]

                if counter > 1:
                    a_x, a_y = np.array([v_x, v_y]) - f_prev[2:4]

            flow[entity_idx, t, :] = [x, y, v_x, v_y, a_x, a_y]
            counter += 1

    return flow
