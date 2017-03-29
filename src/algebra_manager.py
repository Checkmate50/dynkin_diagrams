from src import helper
from functools import partial


def describe_algebra(roots):
    """
    Given a list of vectors 'roots'
    Generates a matrix describing the lie algebra with the given roots

    :param roots:
    :return:
    """

    return roots


def weyl_group(basis):
    """
    Given a list of basis vector 'basis'
    Returns all possible reflections (the complete weyl group) of the given basis

    :param basis:
    :return:
    """

    group = basis.copy()

    for alpha in basis:
        s = partial(helper.reflection, alpha)
        for b in basis:
            current_root = b
            current_root = s(current_root)
            while current_root != b:
                group.append(current_root)
                current_root = s(current_root)

    return group


def recover_roots(basis):
    """
    Given a list of basis vector 'basis'
    Returns a list of the roots of the given basis

    :param basis:
    :return:
    """

    roots = basis.copy()

    for alpha in roots:  # Sketchy, but I'm confident it works
        s = partial(helper.reflection, alpha)
        # Basically, we want to apply every possible combination of reflections until we die
        # Since reflections are commutative, we can just apply them to roots as we build roots
        for b in roots:
            current_root = s(b)
            if current_root not in roots:
                roots.append(current_root)

    return roots


def get_basis(cartan):
    """
    Given a 2-dimensional cartan matrix 'cartan'
    Returns the basis represented by this matrix
    Raises a ValueError if the given matrix is not a cartan matrix
    Note that the given cartan matrix is assumed (without enforcement) to be of the
    format given by the cartan_matrix function in diagram_manager.py

    :param cartan:
    :return:
    """

    size = len(cartan)
    # Contractually verify basic properties of cartan matrix
    for i in range(size):
        if size != len(cartan[i]):
            raise ValueError("Cartan matrix must be square")
        if cartan[i][i] != 2:
            raise ValueError("Cartan matrix must have 2s on the diagonal")
        for j in range(i, size):
            if (cartan[i][j] == 0) ^ (cartan[j][i] == 0):
                raise ValueError("Cartan matrix must have symmetry of 0s")

    basis = []
    skip = 0  # Used to ignore the rest of a block
    block_size = -1  # Keep track of block size for E blocks
    offset = 0  # Keep track of the size of previous blocks

    # Since we have already derived the bases for each possible cartan arrangement,
    # we just generate the basis on a case-by-case basis by what we read in
    for i in range(size - 1):
        block_size += 1

        if skip > 0:
            skip -= 1
            if skip == 0:
                offset += block_size + 1
                block_size = -1
            continue

        # End of A_n
        if cartan[i][i + 1] == 0:
            basis.append([0.0 for _ in range(offset + block_size)] + [1.0, -1.0])
            offset += block_size + 2
            block_size = -1
            continue

        if cartan[i][i+1] == cartan[i+1][i] == -1:
            # Main line case
            if size <= i+2 or not cartan[i][i+2] == cartan[i+2][i] == -1:
                basis.append([0.0 for _ in range(offset + block_size)] + [1.0, -1.0])
                continue
            # E case **MAY NEED TO BE MODIFIED**
            if size > i+3 and cartan[i+2][i+3] == cartan[i+3][i+2] == -1:
                basis.append([0.0 for _ in range(offset + block_size)] + [1.0, -1.0])
                basis.append([0.0 for _ in range(offset + block_size + 1)] + [1.0, -1.0])
                basis.append([0.0 for _ in range(offset)] + [-1.0, -1.0])
                basis.append([0.0 for _ in range(offset)] +
                             [-0.5] + [0.5 for _ in range(6)] + [-0.5])
                skip = 3
                continue
            # D case
            basis.append([0.0 for _ in range(offset + block_size)] + [1.0, -1.0])
            basis.append([0.0 for _ in range(offset + block_size + 1)] + [1.0, -1.0])
            basis.append([0.0 for _ in range(offset + block_size + 1)] + [1.0, 1.0])
            skip = 2
            continue

        if cartan[i][i + 1] == -1:
            # C case
            if cartan[i + 1][i] == -2:
                basis.append([0.0 for _ in range(offset + block_size)] + [1.0, -1.0])
                basis.append([0.0 for _ in range(offset + block_size + 1)] + [2.0])
                skip = 1
                continue
            # G case
            if cartan[i + 1][i] == -3:
                basis.append([0.0 for _ in range(offset + block_size)] + [1.0, -1.0])
                basis.append([0.0 for _ in range(offset + block_size)] + [-2.0, 1.0, 1.0])
                block_size += 1
                skip = 1
                continue
        if cartan[i][i + 1] == -2:
            # F case
            if size > i+2 and cartan[i + 1][i + 2] == cartan[i + 2][i + 1] == -1:
                basis.append([0.0 for _ in range(offset + block_size)] + [1.0, -1.0])
                basis.append([0.0 for _ in range(offset + block_size + 1)] + [1.0])
                basis.append([0.0 for _ in range(offset)] + [-0.5, -0.5, -0.5, 0.5])
                skip = 2
                continue
            # B case
            if cartan[i + 1][i] == -1:
                basis.append([0.0 for _ in range(offset + block_size)] + [1.0, -1.0])
                basis.append([0.0 for _ in range(offset + block_size + 1)] + [1.0])
                skip = 1
                continue
        raise ValueError("Invalid cartan matrix")  # No cases met

    if skip == 0:
        basis.append([0.0 for _ in range(offset + block_size + 1)] + [1.0, -1.0])
    helper.extend_basis(basis)

    return basis

