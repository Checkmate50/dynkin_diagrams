"""
This script provides a collection of simple quality of life function definitions
"""


def reflection(v, x):
    """
    Given a hyperplane vector 'v' and a n-dimensional point 'x'
    Returns the reflection of x across v
    Raises a value exception if the two vectors do not have the same length

    :param v:
    :param x:
    :return:
    """
    return x - 2*(inner_product(x, v)/inner_product(v, v))*v


def angle_product(u, v):
    """
    Given two arrays 'u' and 'v' of the same length
    Returns the angle product <u, v> of the two vectors
    Raises a value exception if the two vectors do not have the same length

    :param u:
    :param v:
    :return:
    """

    return 2*inner_product(u, v)/inner_product(v, v)


def inner_product(vector1, vector2):
    """
    Given two arrays 'vector1' and 'vector2' of the same length
    Returns the euclidean inner product (u, v) of the two vectors
    Raises a value exception if the two vectors do not have the same length

    :param vector1:
    :param vector2:
    :return:
    """

    if len(vector1) != len(vector2):
        raise ValueError("Length of the vectors " + str(vector1) + " and " + str(vector2) + " does not match")
    return sum(vector1[i] * vector2[i] for i in range(len(vector1)))

