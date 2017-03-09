def ddiagram(letter, number):
    """
    Given a dynkin diagram letter and order
    Generates the string associated with that diagram
    Returns 1 if the input did not describe a possible graph

    STYLE:
    o denotes a vertex
    - denotes a single edge
    = denotes a double edge
    ~ denotes a triple edge
    < and > denote directions of double and triple edges
    | replaces o to denote a branch
    """

    letter = str(letter).lower()
    number = int(number)
    if letter not in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
        return 1
    if number < 0:
        return 1
    if letter == "e" and (number > 8 or number < 3):
        return 1
    elif letter == "f" and number != 4:
        return 1
    elif letter == "g" and number != 2:
        return 1

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
            return "o-o-|"
        return "o-o-|-" + ("o-"*(number-4))[:-1]

    if letter == "f":
        return "o-o=>o-o"

    return "o~>o"


def cross(diagrams):
    """
    Given a list of tuples (letter, order)
    Returns the string representation of crossing these diagrams
    Note that newlines deliminate new diagrams
    """

    s = ""
    for diagram in diagrams:
        s += ddiagram(*diagram) + "\n"
    return s.strip()

