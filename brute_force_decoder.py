#!/usr/local/bin/python2.7

"""
# Brute force decoder for Text to Bitmap (Unicode version only)

# Modes:
    # range
    # start_to_finish

# Run duration:
    # set num of tries
    # until stopped (not a special mode ... just stop it when you want!)

# Includes:
    # detailed logging [always on]
    # include # of tries [always on]

"""


def brute_force_decoder(bitmap_to_decode, mode, duration_type, duration, options=None, details=None):

    from uni_text_to_bitmap import uni_decode_image_as_text
    import text_to_bitmap_autogen

    with open(bitmap_to_decode, "rb") as bitmap_file:
        image_bytes = bitmap_file.read()

    if mode == 'range' or mode == 'start_to_finish':

        if mode == 'range' and details is None:
            print "Using the range mode requires details (start and endpoints, length)"
            return False
        elif mode =='start_to_finish':
            details = {'hex_start': '000000',
                       'hex_end': 'ffffff',
                       'avp_min': 4,
                       'avp_max': 24,
                       'rgb_min': 4,
                       'rgb_max': 12,
                       'off_min': 0,
                       'off_max': 65535
                       }

        print "Using the following details: ", details

        try:
            hex_combinations = int(details['hex_end'], 16) - int(details['hex_start'], 16)

            apv_combinations = 0
            for apv_c in xrange(details['avp_min'], details['avp_max']):
                apv_combinations += 5 ** apv_c

            rgb_combinations = 0
            for rgb_c in xrange(details['rgb_min'], details['rgb_max']):
                rgb_combinations += 6 ** rgb_c

            offset_combinations = details['off_max'] - details['off_min']
        except KeyError, e:
            print "Missing important details; cannot run in range mode without: ", e
            return False

        combinations = long(hex_combinations * apv_combinations * rgb_combinations * offset_combinations)

        print "Number of combinations this run is testing for: {0}".format(combinations)

    try_number = 0

    if duration_type == 'set':
            for message in try_to_decode(image_bytes, details):
                if try_number < duration or duration == -1:
                    try_number += 1
                    # Would suppressing this print on failure speed the process up? (Hard to test reliably on this box) If so, consider creating a suppression flag
                    print "[{0}] {1}".format(try_number, message)
                else:
                    print "[END] Reached the end of {0} tries.".format(duration)
                    break
    else:
        print "Duration type or duration is invalid! ({0}, {1})".format(duration_type, duration)
        return False


def try_to_decode(image_bytes, details):

    import text_to_bitmap_autogen
    from uni_text_to_bitmap import uni_decode_image_as_text

    for hexseed in text_to_bitmap_autogen.generate_nonrandom_hexseed(int(details['hex_start'], 16), int(details['hex_end'], 16)):
        for addvalpos in text_to_bitmap_autogen.generate_nonrandom_addvalpos(details['avp_min'], details['avp_max']):
            for rgborder in text_to_bitmap_autogen.generate_nonrandom_rgbscrambling(details['rgb_min'], details['rgb_max']):
                for offset in text_to_bitmap_autogen.generate_nonrandom_offset(details['off_min'], details['off_max']):

                    decoded_text = uni_decode_image_as_text(image_bytes, seed=hexseed, instructions=[offset, addvalpos, rgborder], as_bytes=True)

                    if decoded_text[:39] == '[FAILED] Decode failed for Code Point #':
                        # Now, don't fool the brute force decoder by beginning all of your messages with this.  That would be silly.
                        yield "[FAILED] HX: {0}; AVP: {1}; RO: {2}; OFF: {3}".format(hexseed, addvalpos, rgborder, offset)
                    else:
                        yield "[DECODED!] Using HX: {0}; AVP: {1}; RO: {2}; OFF: {3}; MESSAGE: {4}".format(hexseed, addvalpos, rgborder, offset, decoded_text)


if __name__ == '__main__':

    import sys

    USAGE = '''python brute_force_decoder.py <bitmap> <mode> <duration> [details_file]

    bitmap: filename of encoded bitmap to decode
    mode: string containing range or start_to_finish
    duration: number of tries or -1 to run until terminated (if number of tries is reached before the range is complete, run will terminate)
    details_file: if using in range mode, details file will enumerate value ranges to attempt.  See examples_details_bf.txt for example.

    Example 1: python brute_force_decoder.py secret.bmp range -1 range_details.txt
    Example 2: python brute_force_decoder.py secret.bmp start_to_finish 1000
    '''

    try:
        details = None
        
        bitmap_to_decode = sys.argv[1]
        mode = sys.argv[2]
        duration_type = 'set' # For now; will change later as other modes become available

        if duration_type in ['set']:
            duration = int(sys.argv[3])

        if mode not in ['range', 'start_to_finish']:
            raise IndexError

        if mode == 'range':
            details_filename = sys.argv[4]

            # By default, we will include the whole range -- so if the file reading fails, we at least have something.
            details = {'hex_start': '000000',
                       'hex_end': 'ffffff',
                       'avp_min': 4,
                       'avp_max': 24,
                       'rgb_min': 4,
                       'rgb_max': 12,
                       'off_min': 0,
                       'off_max': 65535
                }

            try:
                with open(details_filename, 'r') as details_file:
                    for detail_line in details_file.readlines():
                        detail_line = detail_line.strip()
                        if detail_line[0] == '#': # Ignore commented lines
                            continue
                        if detail_line[:7] == 'hex_sta':
                            details['hex_start'] = detail_line[10:]
                        elif detail_line[:7] == 'hex_end':
                            details['hex_end'] = detail_line[8:]
                        else:
                            details[detail_line[:7]] = int(detail_line[8:])
            except Exception:
                print "There was an error in reading {0}".format(details_filename)
                sys.exit(1)
                            
        if duration_type not in ['set']:
            raise IndexError
            
    except Exception:
        print USAGE
        sys.exit(1)

    try:
        brute_force_decoder(bitmap_to_decode=bitmap_to_decode, mode=mode, duration_type=duration_type, duration=duration, details=details)
    except KeyboardInterrupt:
        print "\n[ENDING RUN DUE TO KEYBOARD INTERRUPT]"
        sys.exit(0)
