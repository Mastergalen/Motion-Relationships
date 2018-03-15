import numpy as np


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
