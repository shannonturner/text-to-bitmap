import random

def generate_hexseed(n):

    """ Generates n randomly generated values of 000000-FFFFFF.
    """

    for value in xrange(n):       
        yield "{0:0>6x}".format(random.randint(0, 16777216))

def generate_addvalpos(n):

    """ Generates n randomly generated addition value position offsets between 0 and 4.
    """

    for value in xrange(n):
        yield str(random.randint(0, 4))

def generate_rgbscrambling(n):

    """ Generates n randomly generated RGB position scrambles.
    """

    for value in xrange(n):
        yield ''.join(random.sample(['r', 'g', 'b'], 3))

def create_instructions(n):

    """ Generates the instructions according to a set level of strength.
        1: minimum strength; 9: maxmimum strength
    """

    try:
        n = int(n)
    except ValueError:
        n = 9

    if n < 1:
        n = 1

    if n > 9:
        n = 9

    hexseeds = list(generate_hexseed(n + random.randint(1, 1 + n)))
    addvalpos = list(generate_addvalpos(n + random.randint(1, 1 + n*2)))
    rgbscramble = list(generate_rgbscrambling(n + random.randint(1, 1 + n*2)))

    return (hexseeds, addvalpos, rgbscramble)
