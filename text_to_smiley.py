import struct

def distribute_to_rgb(char_value, base_rgb, midpoint=0, deviation=32, random_zeropadding=True):

    " Distributes ord values of char evenly among R, G, and B values, calculated as distance from the midpoint. "

    # RGB value boundaries of 0 and 255 MUST NOT wrap around

    color_distribution = ['r', 'g', 'b']

    distributed = {
        'r': 0,
        'g': 0,
        'b': 0
        }

    char_rgb = []
    char_rgb.extend(base32(char_value))

    while random_zeropadding and len(char_rgb) < 3:

        # This operates on the principle that only the deviance from the base is measured to calculate the char
        
        import random

        char_rgb.insert(random.randint(0,2), 0)

    char_rgb = ''.join([str(c) for c in char_rgb])

    conversion_map = '0123456789abcdefghijklmnopqrstuv'

    distributed['r'] = conversion_map.index(char_rgb[0])
    distributed['g'] = conversion_map.index(char_rgb[1])
    distributed['b'] = conversion_map.index(char_rgb[2])

    for index, color in enumerate(base_rgb):

        if int(color) + int(distributed[color_distribution[index]]) > 255:
            distributed[color_distribution[index]] = int(color) - distributed[color_distribution[index]]
        else:
            distributed[color_distribution[index]] = int(color) + distributed[color_distribution[index]]

    return distributed


def base32(n):

    " Convert n to a 3-char base32 string "

    assert 0 <= n <= 32767

    conversion_map = '0123456789abcdefghijklmnopqrstuv'

    # Depending on whether you end up wanting the leading zero-padding, toggle including/removing the lstrip
    # At the moment I'm leaning toward removing it so I can add randomly-chosen zero-padding

    return ((n == 0) and conversion_map[0]) or (base32(n // 32).lstrip(conversion_map[0]) + conversion_map[n % 32])


def split_in_half(n):

    " Split a number evenly in half, return two whole numbers "

    return ((n // 2), (n - (n // 2)))


def alter_base(base_image_filename, altered_image_filename, message):

    " Opens the base image and alters it to hide the message. "

    import text_to_smiley_debug

    message = [m for m in message]

    if len(message) > 84:
        print "[NOTICE] Only messages of 84 or fewer characters may be entered.  Message will be truncated."
        message = message[:84]

    base_header, base_values, base_end_bytes = text_to_smiley_debug.read_bmp(base_image_filename)
    image_width = list(struct.unpack("<B", base_header[18])).pop() # width is located in header[18]

    skip_end_byte = 0

    sextuplet = []
    output = []

    color_order = ['r', 'g', 'b']

    for index, char in enumerate(base_values):

        skip_end_byte += 1

        if skip_end_byte == image_width * 3:
            skip_end_byte = 0
            output.append(struct.pack("<B", 255)) # This clears out most of the corruption, except for 0,4 and 1,4

        sextuplet.append(char)

        if len(sextuplet) == 6 or (index == 506 and len(sextuplet) == 3):

            if len(message) > 0:
                message_char = message.pop(0)
                message_values = split_in_half(ord(message_char))

                for mv_index, message_value in enumerate(message_values):
                    if mv_index == 0:
                        alter_rgb = distribute_to_rgb(message_value, sextuplet[:3])
                    else:
                        alter_rgb = distribute_to_rgb(message_value, sextuplet[3:])

                    for color in color_order:
                        output.append(struct.pack("<B", alter_rgb[color]))
            else:

                for triplet in xrange(2):

                    try:
                        alter_rgb = {'r': int(sextuplet[(triplet * 3) + 0]),
                                     'g': int(sextuplet[(triplet * 3) + 1]),
                                     'b': int(sextuplet[(triplet * 3) + 2])
                                     }
                    except IndexError:
                        alter_rgb = {'r': int(sextuplet[0]),
                                     'g': int(sextuplet[1]),
                                     'b': int(sextuplet[2])
                                     }

                    for color in color_order:
                        output.append(struct.pack("<B", alter_rgb[color]))

            sextuplet = []

    output.append(struct.pack("<B", 255))

    with open(altered_image_filename, 'wb') as altered_image_file:
        altered_image_file.write(base_header)
        altered_image_file.write(''.join(output))
