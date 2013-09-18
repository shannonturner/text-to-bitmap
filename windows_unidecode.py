# This is meant to be run in IDLE or another IDE - not by command line.
# Windows Command line has a compatibility issue with displaying UTF-8 characters.
# This is the workaround.

import sys
from uni_text_to_bitmap import *

sys.argv = ['python uni_text_to_bitmap.py', 'decode', 'secret2.bmp', 'feeb1e', [33, '4231020204104', 'gbr,rbg,grb,gbr,gbr,rgb,brg']] #  Change these values here.

bitmap_filename = sys.argv[2]
hexseed = sys.argv[3]
instructions = sys.argv[4]  # Contains Offset, Addition Value Positions, RGB Scrambling

print u"{0}".format(uni_decode_image_as_text(bitmap_filename, hexseed, instructions))
