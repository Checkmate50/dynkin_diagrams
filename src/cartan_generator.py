def get_roots(algebra):
    """
    Given a lie algebra
    Returns a list of the roots of that algebra

    :param algebra:
    :return:
    """

    return algebra


def get_basis(roots):
    """
    Given a list of roots
    Returns a list of the basis vectors corresponding to those roots

    :param roots:
    :return:
    """

    return roots


def gen_cartan(basis):
    """
    Given a list of the basis elements of a lie algebra
    Returns the cartan matrix associated with that lie algebra

    :param basis:
    :return:
    """

    size = len(basis)
    to_return = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            to_return[i][j] = int(angle_product(basis[i], basis[j]))
    return to_return


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
    Returns the Euclidian inner product of the two vectors
    Raises a value exception if the two vectors do not have the same length

    :param vector1:
    :param vector2:
    :return:
    """

    if len(vector1) != len(vector2):
        raise ValueError("Length of the vectors " + str(vector1) + " and " + str(vector2) + " does not match")
    return sum(vector1[i] * vector2[i] for i in range(len(vector1)))

