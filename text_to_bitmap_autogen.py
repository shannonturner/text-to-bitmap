#!/usr/local/bin/python2.7

import itertools
import random

def generate_hexseed(n):

    """ Generates n randomly generated values of 000000-FFFFFF.
    """

    for value in xrange(n):       
        yield "{0:0>6x}".format(random.randint(0, 16777216))

def generate_nonrandom_hexseed(start=0, end=16777216):

    " Generates non-randomly generated hex values of between the accepted ranges of 000000-FFFFFF. "

    assert start >= 0
    assert end <= 16777216
    assert start < end

    for value in xrange(start, end + 1):
        yield "{0:0>6x}".format(value)

def generate_addvalpos(n):

    """ Generates n randomly generated addition value position offsets between 0 and 4.
    """

    for value in xrange(n):
        yield str(random.randint(0, 4))

def generate_nonrandom_addvalpos(min_length=4, max_length=24):

    " Generates non-randomly generated addition value position offsets between 0 and 4, between the min_length and max_length.  Minimum and maximum length contain the default range provided by the API."

    permutations = [str(x) for x in range(5)]

    for current in xrange(min_length, max_length + 1):
        yield [''.join(avp) for avp in itertools.product(permutations, repeat=current)]


def generate_rgbscrambling(n):

    """ Generates n randomly generated RGB position scrambles.
    """

    for value in xrange(n):
        yield ''.join(random.sample(['r', 'g', 'b'], 3))

def generate_nonrandom_rgbscrambling(min_length=4, max_length=12):

    " Generates non-randomly generated rgb scrambling ordering values, between the min_length and max_length.  Minimum and maximum length contain the default range provided by the API."

    permutations = [''.join(rgborder) for rgborder in itertools.permutations('ABC')]

    for current in xrange(min_length, max_length + 1):
        yield [','.join(grouping) for grouping in itertools.product(permutations, repeat=current)]

def generate_nonrandom_offset(start=32, end=65535):

    " Generates non-randomly generated universally-applied offsets between start and end. "

    for offset in xrange(start, end + 1):
        yield offset

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
