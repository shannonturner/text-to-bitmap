# uni_text_to_bitmap.py: Adds unicode support

import codecs
import math
import random
import struct
import sys
from text_to_bitmap import factors, get_dimensions, bmp_write, row_padding, map_color, map_hexcolor, plot_points

def uni_simple_encode(string, debug_mode=False):

    """ uni_simple_encode(string): Unicode-enabled version of text_to_bitmap.simple_encode().  Encodes each character as two ord values.
    """

    ords = []
    ord_values = []

    for char in string:
        if ord(char) > 32:
            ord_values.append(ord(char))

    min_ord = min(ord_values) - 2
    
    for (index, ord_value) in enumerate(ord_values):
        ords.extend(split_number(ord_value - min_ord))

    print "\nTO DECODE YOUR MESSAGE YOU WILL NEED THE OFFSET: {0}\n".format(min_ord)

    if debug_mode:
        return (ords, ord_values)
    else:        
        return ords

def split_factors(n):

    """ split_factors(n): Used to split a factor to get it below 256
    """ 

    factor_list = list(factors(n))
    factor_list.sort()

    if len(factor_list) == 2: # n is prime
        return factor_list
    elif len(factor_list) > 2:

        choose_from = factor_list[1:-1] # Remove 1 and n - add_value from the set of factors

        while len(choose_from) > 4:
            choose_from.pop(len(choose_from)-1)
            choose_from.pop(0)

        chosen = random.choice(choose_from)
        chosen_pair = n / chosen

        return (chosen, chosen_pair)
    else:
        if n == 1:
            return (1, 1)

def remove_large_primes(factor_list, n):

    """ remove_large_primes(factor_list, n): Removes prime numbers greater than 255 from the factor list, as well as their pairs.  Returns the scrubbed factor list.
    """

    for (index, factor) in enumerate(factor_list):
        if len(list(factors(factor))) == 2 and factor > 255:
            factor_list.remove(factor)
            factor_list.remove(n / factor)            

    return factor_list

def get_factors(n):

    """ get_factors(n): Gets a suitable set of factors that can be used in the rest of the calculations.
    """

    assert n > 1

    if n > 255:
        add_value = random.randint(1, 255)
    else:
        add_value = random.randint(1, (n - 1))
    
    factor_list = list(factors(n - add_value))

    while n > 255 and len(factor_list) == 2: # Recalculate if the number is prime
        add_value = random.randint(1, 255)
        factor_list = list(factors(n - add_value))       
    
    factor_list.sort()

    if len(factor_list) > 2:
        choose_from = factor_list[1:-1] # Remove 1 and n - add_value from the set of factors
    else:
        choose_from = factor_list

    return (add_value, choose_from)

def split_number(n):

    """ split_number(n): Splits a number into four multiples and an additional random value that is added to the multiplied value to get the original
    """

    return_factors = []

    while return_factors == [] or (True in [True for x in return_factors if x > 255]): # If there is a value > 255, recalculate.

        return_factors = []

        (add_value, choose_from) = get_factors(n)

        # Remove prime factors larger than 255
        choose_from = remove_large_primes(choose_from, n - add_value)
        while len(choose_from) == 0:
            (add_value, choose_from) = get_factors(n) # Recalculate

        while len(choose_from) > 4: # While there are more than 4 sets of factors remaining
            choose_from.pop(len(choose_from)-1) # Pop the highest value
            choose_from.pop(0) # Pop the highest value's pair

        # In all cases, select the factor to use.
        chosen = random.choice(choose_from)
        chosen_pair = (n - add_value) / chosen
        
        # Now, factor the chosen and chosen pair and add those
        return_factors.extend(split_factors(chosen))
        return_factors.extend(split_factors(chosen_pair))

        return_factors.append(add_value)

    return return_factors

def rgb_triplets(ords, seed, instructions=None):

    """ rgb_triplets(ords, seed, instructions): Creates the r, g, and b values from the ords, using seed as r, g, and b offsets.
    """

    (rseed, gseed, bseed) = (int(seed[0:2], base=16), int(seed[2:4], base=16), int(seed[4:6], base=16))

    assert 0 <= rseed <= 255
    assert 0 <= gseed <= 255
    assert 0 <= bseed <= 255

    if instructions is not None:
        rgb_instructions = instructions[1].replace('"', '').replace("'","").split(",")

    seeds = {'r': rseed, 'g': gseed, 'b': bseed}

    colors = []

    while len(ords) > 0:

        rgb_instruction = rgb_instructions.pop(0)
        rgb_instructions.append(rgb_instruction)

        offset = [None, None, None]

        for index, color in enumerate(rgb_instruction):
            offset[index] = seeds[color]           

        r = ords.pop()
        try:
            g = ords.pop()
        except IndexError:
            g = 0
        try:
            b = ords.pop()
        except IndexError:
            b = 0

        if r + offset[0] < 256:
            r += offset[0]
        else:
            r += offset[0] - 255

        if g + offset[1] < 256:
            g += offset[1]
        else:
            g += offset[1] - 255

        if b + offset[2] < 256:
            b += offset[2]
        else:
            b += offset[2] - 255

        colors.append((r,g,b))
    
    return colors



def uni_encode_text_as_image(text_filename, image_filename, seed = "000000", instructions = None, debug_mode = False, minheight = 4, maxheight = False):

    """ uni_encode_text_as_image(text_filename, image_filename, seed, instructions, minheight, maxheight): Encodes Unicode text as a bitmap.  Each character is five rgb values (r, g, b, r, g).
            Seed is used to offset the R, G, B values as a layer of security.
            Instructions contains the addition position instructions and the RGB value scrambling instructions
            Minimum height of 4 prevents unnecessary padding.
            NOTE: Text files that are very small may not be large enough to encode properly into a valid bitmap.
    """

    with codecs.open(text_filename, encoding='utf-8', mode="rb") as text_file:
        text = text_file.read().replace("\n", "")

    if instructions is not None:
        addition_position_instructions = list(instructions[0].replace("'","").replace('"',''))

    if debug_mode:
        (ord_values, debug_original_ords) = uni_simple_encode(text, debug_mode)
    else:
        ord_values = uni_simple_encode(text)

    if instructions is not None:

        scrambled_ord_values = []
        ord_start = 0
        ord_stop = 5

        while ord_stop < len(ord_values):

            position = int(addition_position_instructions.pop(0))
            addition_position_instructions.append(position)

            temp_ords = ord_values[ord_start:ord_stop]
            addition_value = temp_ords.pop(4)

            random.shuffle(temp_ords)
            temp_ords.insert(position, addition_value)

            scrambled_ord_values.extend(temp_ords)

            ord_start += 5
            ord_stop +=5

        ord_values = scrambled_ord_values

    ord_values.reverse() # Colors are mapped in 'reverse' order.

    if debug_mode:
        import copy
        debug_ord_values = copy.deepcopy(ord_values)
            
    color_triplets = rgb_triplets(ord_values, seed, instructions)    
    (width, height) = get_dimensions(color_triplets, minheight, maxheight)

    if debug_mode:
        
        with open('debug_encode.csv', 'w') as debug_encode_file:

            # Write the header.  It's a csv, so use abbreviations to preserve column width
            debug_encode_file.write('---,ORG,---,|||,---,POS,---,|||,---,ENC,---\n') # Three columns for the original ords, three for the 5 split/position scrambled values, three for the encoded values

            original_triplets = []
            original_triplet = []
            # Make into unencoded triplets
            for debug_ord_value in debug_ord_values:
                original_triplet.append(debug_ord_value)

                if len(original_triplet) == 3:
                    original_triplets.append(original_triplet)
                    original_triplet = []

            else:
                if original_triplet != []:
                    while len(original_triplet) < 3:
                        original_triplet.append(0)

                    original_triplets.append(original_triplet)

            while len(debug_original_ords) < len(original_triplets):
                debug_original_ords.append('') # to use with zip

            for (original_ord, original_triplet, encoded_triplet) in zip(debug_original_ords, original_triplets, color_triplets):
                debug_encode_file.write(',{0},,|||,{1},|||,{2}\n'.format(original_ord, ','.join([str(og3) for og3 in original_triplet]), ','.join([str(ec3) for ec3 in encoded_triplet])))
        
    pixels = plot_points(width, height, color_triplets)

    bmp_header = {'mn1':66,
        'mn2':77,
        'filesize':0,
        'undef1':0,
        'undef2':0,
        'offset':54,
        'headerlength':40,
        'width':width,
        'height':height,
        'colorplanes':1,
        'colordepth':24,
        'compression':0,
        'imagesize':(width * height * 3),
        'res_hor':0,
        'res_vert':0,
        'palette':0,
        'importantcolors':0}

    bmp_write(bmp_header, ''.join(pixels), image_filename)

    return

def uni_decode_image_as_text(image_filename, seed = "000000", instructions = None, debug_mode = False):

    """ uni_decode_image_as_text(image_filename, seed, instructions): Decodes a bitmap image produced by uni_encode_text_as_image() as long as the seed and instruction values are correct.
            Instructions contains in order:
            [0]: The offset printed when encoding
            [1]: The addition value positions to unscramble
            [2]: The RGB scrambling values
    """

    (rseed, gseed, bseed) = (int(seed[0:2], base=16), int(seed[2:4], base=16), int(seed[4:6], base=16))

    assert 0 <= rseed <= 255
    assert 0 <= gseed <= 255
    assert 0 <= bseed <= 255

    with open(image_filename, "rb") as decode_file:
        discard_header = decode_file.read(54)

        decoded_text = []

        character_counter = 0
        original_value = 1

        if instructions is None:
            rgbseeds = [rseed, gseed, bseed]
        else:

            offset = instructions[0]
            addition_value_positions = list(instructions[1])
            rgb_value_positions = instructions[2]

            rgbseeds = []
            for rgb_value_position in rgb_value_positions:
                if rgb_value_position.lower() == 'r':
                    rgbseeds.append(rseed)
                elif rgb_value_position.lower() == 'g':
                    rgbseeds.append(gseed)
                elif rgb_value_position.lower() == 'b':
                    rgbseeds.append(bseed)        

        characters = {
                'read_from_file': [],
                'rgb_offset_applied': [],
                'groups_of_five': []
            }
        groups_of_five = []

        # Loop through and obtain bytes; skip row_padding() bytes
        for byte in decode_file.read():

            char = list(struct.unpack("<B", byte)).pop()

            if char == 0: # Ignore any row_padding() bytes
                continue

            characters['read_from_file'].append(char)

        characters['read_from_file'].reverse()

        if debug_mode:
            import copy
            still_encoded = copy.deepcopy(characters['read_from_file'])

        # Apply RGB offsets
        for char in characters['read_from_file']:

            rgbseed = rgbseeds.pop(0)
            rgbseeds.append(rgbseed)

            if (char - rgbseed) < 0:
                char -= rgbseed
                char += 255
            else:
                char -= rgbseed

            characters['rgb_offset_applied'].append(char)

        # Clump into groups of five
        for char in characters['rgb_offset_applied']:

            groups_of_five.append(char)

            if len(groups_of_five) == 5:
                characters['groups_of_five'].append(groups_of_five)
                groups_of_five = []
        else:
            if len(groups_of_five) > 0:
                characters['groups_of_five'].append(groups_of_five)

        if debug_mode:
            decoded_values = []

        # Apply addition value position unscrambling and decode                        
        for group_of_five in characters['groups_of_five']:

            addition_value_position = int(addition_value_positions.pop(0))
            addition_value_positions.append(addition_value_position)

            if len(group_of_five) == 5:
                addition_value = group_of_five.pop(addition_value_position)
                group_of_five.append(addition_value)
            else:
                while len(group_of_five) < 4:
                    group_of_five.append(1) # Multiplication value
                else:
                    group_of_five.append(0) # Addition value
                    
            for char in group_of_five:

                character_counter += 1

                if character_counter < 5:
                    original_value *= char
                    
                elif character_counter == 5:

                    original_value += char

                    try:
                        decoded_text.append(unichr(original_value + offset))
                        if debug_mode:
                            decoded_values.append(original_value + offset)
                    except ValueError:
                        return "[FAILED] Decode failed for Code Point #{0}; confirm that you are using the correct RGB seeds, addition value positions, and RGB value positions.".format(original_value + offset)
                    
                    character_counter = 0
                    original_value = 1

        if debug_mode:

            with open('debug_decode.csv', 'w') as debug_decode_file:

                # Write the header.  It's a csv, so use abbreviations to preserve column width
                debug_decode_file.write('---,ENC,---,|||,---,DEC,---\n') # Three columns for the still-encoded values, three for the decoded values

                encoded_triplets = []
                encoded_triplet = []

                for still_encoded_value in still_encoded:
                    encoded_triplet.append(still_encoded_value)

                    if len(encoded_triplet) == 3:
                        encoded_triplets.append(encoded_triplet)
                        encoded_triplet = []

                # There will be 5x fewer decoded numbers since there are four multiplication values and an addition value to create each one
                while len(decoded_values) < len(still_encoded):
                    decoded_values.append('') # This will let me use zip below.

                decoded_triplets = []
                decoded_triplet = []

                for decoded_value in decoded_values:
                    decoded_triplet.append(decoded_value)

                    if len(decoded_triplet) == 3:
                        decoded_triplets.append(decoded_triplet)
                        decoded_triplet = []

                for (encoded_triplet, decoded_triplet) in zip(encoded_triplets, decoded_triplets):
                    debug_decode_file.write('{0},|||,{1}\n'.format(','.join([str(ec3) for ec3 in encoded_triplet]), ','.join([str(dc3) for dc3 in decoded_triplet])))

    return ''.join(decoded_text) 

if __name__ == '__main__':

    try:

        # I'm not including this in the Usage string, but this feature now exists.
        if 'debug' in str(sys.argv[1]).lower():
            debug_mode = True
        else:
            debug_mode = False
        
        if 'encode' in str(sys.argv[1]).lower():
            encode_or_decode = "Encode"
            text_filename = sys.argv[2]
            bitmap_filename = sys.argv[3]
            hexseed = sys.argv[4]
            addition_value_positions = sys.argv[5]
            rgb_value_positions = sys.argv[6]

            instructions = [addition_value_positions, rgb_value_positions]

            minimum_height = 4
            maximum_height = False

            if debug_mode:
                print "[DEBUG MODE ENABLED] -- THE STEPS TAKEN TO ENCODE YOUR FILE WILL BE SAVED AS debug_encode.csv"
            
        elif 'decode' in str(sys.argv[1]).lower():
            encode_or_decode = "Decode"
            bitmap_filename = sys.argv[2]
            hexseed = sys.argv[3]
            offset = sys.argv[4]
            addition_value_positions = sys.argv[5]
            rgb_value_positions = sys.argv[6]

            instructions = [offset, addition_value_positions, rgb_value_positions]

            if debug_mode:
                print "[DEBUG MODE ENABLED] -- THE STEPS TAKEN TO DECODE YOUR FILE WILL BE SAVED AS debug_decode.csv"
        else:
            raise IndexError

        if len(sys.argv) >= 8:
            minimum_height = sys.argv[7] # Optional

        if len(sys.argv) == 9:
            maximum_height = sys.argv[8] # Optional; if there is a conflict, maximum height takes precedence over minimum height

    except IndexError:

        print """\nParameters for text_to_bitmap.py:
        To Encode Unicode Text as a Bitmap: encode textfile, bitmap_file, secret_hexseed, addition_value_position, rgb_value_position, [minimum_height = 4] [maximum_height]
        Example: python uni_text_to_bitmap.py encode "encodeme.txt" "secret.bmp" afb391 "2420130201202302134" "gbr,rgb,brg,gbr"

        To Decode a Bitmap into Unicode Text: decode bitmap_file, secret_hexseed, instructions(offset, addition value position, rgb value position)
        Example: python uni_text_to_bitmap.py decode "secret.bmp" afb391 932 "2420130201202302134" "gbr,rgb,brg,gbr" """
        
        sys.exit(1)   

    if encode_or_decode == 'Encode':
        uni_encode_text_as_image(text_filename, bitmap_filename, hexseed, instructions, debug_mode, minimum_height, maximum_height)
    elif encode_or_decode == 'Decode':
        try:
            print u"{0}".format(uni_decode_image_as_text(bitmap_filename, hexseed, instructions, debug_mode))
        except UnicodeEncodeError:
            print "There is a compatibility issue with the Windows console not supporting UTF-8; see http://stackoverflow.com/a/6789057 for more details.  If you run this with Windows, use IDLE or your favorite IDE to run this."
