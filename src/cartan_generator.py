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

