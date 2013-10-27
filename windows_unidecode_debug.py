# This is meant to be run in IDLE or another IDE - not by command line.
# Windows Command line has a compatibility issue with displaying UTF-8 characters.
# This is the workaround.

import sys
from uni_text_to_bitmap import *

print "[DEBUG MODE ENABLED] -- THE STEPS TAKEN TO DECODE YOUR FILE WILL BE SAVED AS debug_decode.csv"

sys.argv = ['python uni_text_to_bitmap.py', 'debugdecode', 'debugtest.bmp', '012345', [932, '01221020102034', 'grb,gbr,brg']]

if 'debug' in str(sys.argv[1]).lower():
    debug_mode = True
else:
    debug_mode = False

bitmap_filename = sys.argv[2]
hexseed = sys.argv[3]
instructions = sys.argv[4]  # Contains Offset, Addition Value Positions, RGB Scrambling

print u"{0}".format(uni_decode_image_as_text(bitmap_filename, hexseed, instructions, debug_mode))
