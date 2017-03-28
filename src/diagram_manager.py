def ddiagram(letter, number=-1):
    """
    Given a dynkin diagram letter and positive number
    Or the letter and number as a single string
    Generates the string associated with that diagram
    Returns "invalid graph" if the input did not describe a possible graph

    STYLE:
    o denotes a vertex
    - denotes a single edge
    = denotes a double edge
    ~ denotes a triple edge
    < and > denote directions of double and triple edges
    | replaces o to denote a branch

    :param letter:
    :param number:
    :return:
    """

    letter = str(letter).lower()
    number = int(number)
    if number == -1:
        number = int(letter[1:])
        letter = letter[0]
    if letter not in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
        raise ValueError("invalid graph")
    if number <= 0:
        raise ValueError("invalid graph")

    if letter == "e" and (number > 8 or number < 3):
        raise ValueError("invalid graph")
    if letter == "f" and number != 4:
        raise ValueError("invalid graph")
    if letter == "g" and number != 2:
        raise ValueError("invalid graph")

    if number == 1:
        return "o"

    if letter == "a":
        return ("o-"*number)[:-1]

    if letter == "b":
        return ("o-"*(number-1))[:-1]+"=>o"

    if letter == "c":
        return ("o-"*(number-1))[:-1]+"<=o"

    if letter == "d":
        if number == 2:
            return "o\no"
        if number == 3:
            return "|-o"
        return ("o-"*(number-3))[:-1]+"-|-o"

    if letter == "e":
        if number == 3:
            return "o-o\no"
        if number == 4:
            return "o-o-o-o"
        if number == 5:
            return "o-o-|-o"
        return ("o-"*(number-4))[:-1] + "-|-o-o"

    if letter == "f":
        return "o-o=>o-o"

    return "o<~o"


def cross(diagrams):
    """
    Given a list of tuples (letter, number) or strings
    Returns the string representation of crossing these diagrams
    Note that newlines deliminate new diagrams

    :param diagrams:
    :return:
    """

    s = ""
    for diagram in diagrams:
        if isinstance(diagram, tuple):
            s += ddiagram(*diagram) + "\n"
        else:
            s += ddiagram(diagram) + "\n"
    return s.strip()


def cartan_matrix(diagrams):
    """
    Given a string representation of a dynkin diagram
    Or a list of string representations of dynkin diagrams
    Returns the associated cartan matrix as a 2-dimensional array
    Raises a value exception if the given string includes invalid characters

    :param diagrams:
    :return:
    """

    if isinstance(diagrams, list):
        diagrams = "\n".join(list(map(str, diagrams)))
    else:
        diagrams = str(diagrams)

    size = diagrams.count("o") + 2 * diagrams.count("|")
    if size == 0:
        raise ValueError("Invalid String " + diagrams)
    cartan = [[2 if i == j else 0 for i in range(size)] for j in range(size)]

    count = 0
    for diagram in diagrams.split("\n"):
        allowed = {"o", "-", "=", "~", ">", "<", "|"}

        left = False
        skip = False
        for c in diagram:
            if c not in allowed:
                raise ValueError("Invalid String:\n" + diagram)
            if c == "-":
                count += 1
                if skip:
                    cartan[count - 2][count] = cartan[count][count - 2] = -1
                else:
                    cartan[count - 1][count] = cartan[count][count - 1] = -1
                skip = False

            elif c == "=" or c == "~":
                value = -2 if c == "=" else -3
                count += 1
                cartan[count - 1][count] = cartan[count][count - 1] = -1
                if left:
                    cartan[count][count - 1] = value
                else:
                    cartan[count - 1][count] = value
                left = False

            elif c == "<":
                left = True

            elif c == "|":
                count += 1
                skip = True
                cartan[count - 1][count] = cartan[count][count - 1] = -1
        count += 1

    return cartan


def cartan_diagram(cartan):
    """
    Given a cartan matrix as a 2-dimensional array
    Returns the string representation of the associated dynkin diagram(s)
    If there are multiple diagrams, they are delimited with newlines
    Raises a ValueError of the given matrix is not a valid cartan matrix

    :param cartan:
    :return:
    """

    allowed_values = [-1, -2, -3]
    # lines is an array of arrays of tuples indicating what each point is connected to
    # That is, lines[i] = [(point, count)...], count is the number of lines from a to b (sign indicates direction)
    points = [[] for _ in range(len(cartan))]

    # Assemble the lines array by recording each i,j value
    # Note that we check the requirements of dynkin diagrams in this construction
    for i in range(len(cartan)):
        if len(cartan[i]) != len(cartan):
            raise ValueError("Matrix must be square")
        for j in range(len(cartan[i])):
            if i == j:
                if cartan[i][j] != 2:
                    raise ValueError("Given matrix does not have a 2 (required) at (" + str(i) + ", " + str(j) + ")")
                continue
            if cartan[i][j] == 0:
                continue
            if cartan[i][j] not in allowed_values:
                raise ValueError("Given matrix does not have a value of -1, -2, or -3\
                 at (" + str(i) + ", " + str(j) + ")")
            if cartan[j][i] == 0:
                raise ValueError("The line from " + str(i) + " to " + str(j) + " is not reciprocated")
            points[i].append((j, cartan[i][j]))
            if sum(map(lambda x : x[1], points[i])) <= -4:
                ValueError("Point " + str(i) + " has more than 3 lines extending from it")

    to_return = ""

    # Construct the diagrams based on the line relationships found above
    while True:
        # Keep running through our list of points until we run out of points (have constructed all the diagrams)
        no_points = True
        for point in points:
            if point != 0:
                no_points = False
                break
        if no_points:
            return to_return.strip()
        diagram_points = []
        # Find an endpoint
        for i in range(len(points)):
            if points[i] == 0:
                continue
            if len(points[i]) == 1 or len(points[i]) == 0:
                diagram_points.append(i)
                break
        if len(diagram_points) == 0:
            raise ValueError("No endpoint found (most likely there is a cycle) in the given matrix")

        diagram = "o"
        # Else we have a trivial case
        if len(points[diagram_points[0]]) != 0:
            # Build the diagram, starting with the found endpoint
            current_index = points[diagram_points[0]][0][0]
            current_point = points[current_index]
            size1 = points[diagram_points[0]][0][1]
            size2 = __get_size__(current_point, diagram_points[0])
            diagram_points.append(current_index)
            current_point = current_point.copy()
            diagram += __gen_connector__(size1, size2)
            current_point.remove((diagram_points[0], size2))

            while len(current_point) != 0:
                # Branch case
                next_index = current_point[0][0]
                next_point = points[next_index]
                size1 = current_point[0][1]
                if len(current_point) == 1:
                    diagram += "o"
                else:
                    # Branch case
                    diagram += "|"
                    if len(next_point) == 1:
                        diagram_points.append(next_index)
                        next_index = current_point[1][0]
                        next_point = points[next_index]
                        size1 = current_point[1][1]
                    elif len(points[current_point[1][0]]) > 1:
                        raise ValueError("This matrix gives an extending branch")
                size2 = __get_size__(next_point, current_index)
                diagram_points.append(next_index)
                diagram += __gen_connector__(size1, size2)

                current_point = next_point.copy()
                current_point.remove((current_index, size2))
                current_index = next_index

        to_return += diagram + ("\n" if diagram == "o" else "o\n")
        # Remove points we've already used
        for index in diagram_points:
            points[index] = 0


def __get_size__(point, index):
    """
    Helper function for cartan_diagram
    Given a point 'point' and an index
    Returns the inner product from 'point' to that index

    :param arr:
    :param index:
    :return:
    """

    for line in point:
        if line[0] == index:
            return line[1]


def __gen_connector__(size1, size2):
    """
    Helper function for cartan_diagram
    Given the inner product size between the points 'point1' and 'point2'
    Returns the diagram string representing this connection in a dynkin diagram

    :param point1:
    :param point2:
    :return:
    """

    lines = size1 * size2
    if lines == 1:
        return "-"
    connector = "=" if lines == 2 else "~"
    if size1 < size2:
        return connector + ">"
    return "<" + connector

