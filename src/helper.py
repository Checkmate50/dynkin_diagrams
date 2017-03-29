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
    return add_vectors(x, scale(v, -2*(inner_product(x, v)/inner_product(v, v))))


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


def extend_basis(basis):
    """
    Given a basis, extends the basis to consistent dimensions

    :param basis:
    :return:
    """

    if not basis:  # if basis == []
        return
    dimension = max(len(b) for b in basis)
    for i in range(len(basis)):
        while len(basis[i]) < dimension:
            basis[i].append(0.0)


def add_vectors(vector1, vector2):
    """
    Given two arrays 'vector1' and 'vector2' of the same length
    Returns the sum of the two vectors
    Raises a value exception if the two vectors do not have the same length

    :param vector1:
    :param vector2:
    :return:
    """

    if len(vector1) != len(vector2):
        raise ValueError("Length of the vectors " + str(vector1) + " and " + str(vector2) + " does not match")
    return list(vector1[i] + vector2[i] for i in range(len(vector1)))


def scale(vector, constant):
    """
    Given an array 'vector' and a constant
    Returns the vector with each element scaled by the constant
    Raises a value exception if the two vectors do not have the same length

    :param vector:
    :param constant:
    :return:
    """

    return list(vector[i] * constant for i in range(len(vector)))

