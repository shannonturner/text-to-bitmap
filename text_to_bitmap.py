import math
import struct
import sys  

def simple_encode(string):

    ords = []

    for char in string:        
        ords.append(ord(char))
        
    return ords

def factors(n):    
    return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(math.sqrt(n)) + 1) if n % i == 0)))

def rgb_triplets(ords, seed):

    (rseed, gseed, bseed) = (int(seed[0:2], base=16), int(seed[2:4], base=16), int(seed[4:6], base=16))

    assert 0 <= rseed <= 255
    assert 0 <= gseed <= 255
    assert 0 <= bseed <= 255

    colors = []

    while len(ords) > 0:

        r = ords.pop()
        try:
            g = ords.pop()
        except IndexError:
            g = 0
        try:
            b = ords.pop()
        except IndexError:
            b = 0

        if r + rseed < 256:
            r += rseed
        else:
            r += rseed - 255

        if g + gseed < 256:
            g += gseed
        else:
            g += gseed - 255

        if b + bseed < 256:
            b += bseed
        else:
            b += bseed - 255
        
        colors.append((r,g,b))
    
    return colors

def get_dimensions(colors, minheight = 4, maxheight = False):

    if maxheight == False:
        # Can this be made into a square?
        if math.sqrt(len(colors)) % 1 == 0:
            width = height = int(math.sqrt(len(colors)))
        else:
            factor_set = list(factors(len(colors)))
            factor_set.sort()
            width = int(factor_set[len(factor_set) / 2])
            height = int(factor_set[(len(factor_set) / 2) - 1])

            if height < minheight: # Recalculate
                height = int(minheight)
                width = (len(colors) / height) + 1
    else:
        height = int(maxheight)
        width = (len(colors) / height) + 1        

    return (width, height)

def bmp_write(bmp_header, pixels, filename):
    
    header = []
    header.append(struct.pack('<B', bmp_header['mn1']))
    header.append(struct.pack('<B', bmp_header['mn2']))
    header.append(struct.pack('<L', bmp_header['filesize']))
    header.append(struct.pack('<H', bmp_header['undef1']))
    header.append(struct.pack('<H', bmp_header['undef2']))
    header.append(struct.pack('<L', bmp_header['offset']))
    header.append(struct.pack('<L', bmp_header['headerlength']))
    header.append(struct.pack('<L', bmp_header['width']))
    header.append(struct.pack('<L', bmp_header['height']))
    header.append(struct.pack('<H', bmp_header['colorplanes']))
    header.append(struct.pack('<H', bmp_header['colordepth']))
    header.append(struct.pack('<L', bmp_header['compression']))
    header.append(struct.pack('<L', bmp_header['imagesize']))
    header.append(struct.pack('<L', bmp_header['res_hor']))
    header.append(struct.pack('<L', bmp_header['res_vert']))
    header.append(struct.pack('<L', bmp_header['palette']))
    header.append(struct.pack('<L', bmp_header['importantcolors']))
    header = ''.join(header)

    with open(filename, 'wb') as write_file:
        write_file.write(header)
        write_file.write(pixels)
        
    return
    
def row_padding(width, colordepth):
    
    """ row_padding(width, colordepth): Returns byte padding if necessary to complete the row
    """
    
    byte_length = width * colordepth / 8    
    padding = (4 - byte_length) % 4 

    padbytes = []
    for pad in xrange(padding):
        pad = struct.pack('<B', 0)
        padbytes.append(pad)
        
    return ''.join(padbytes)
    
def map_color(red, green, blue):

    """ map_color(red, green, blue): Maps RGB values to the struct; valid values are from 0-255
    """
    
    return struct.pack('<BBB', red, green, blue)

def map_hexcolor(hexcolor):

    """ map_hexcolor(hexcolor): Maps RGB values from hex to the struct; valid values are from 00-FF.  Accepts hexcolors as either #xxxxxx or xxxxxx.
    """

    assert len(hexcolor) in (6,7)

    if len(hexcolor) == 6:
        start = 0
    elif len(hexcolor) == 7:
        start = 1
        
    red = int(hexcolor[start:start+2], base=16)
    green = int(hexcolor[start+2:start+4], base=16)
    blue = int(hexcolor[start+4:start+6], base=16)
    
    return map_color(red, green, blue)

def plot_points(width, height, colors):

    pixels = []
    
    for x in xrange(width):
        for y in xrange(height):
            try:
                (b, g, r) = colors.pop()
            except IndexError:
                (b, g, r) = (0, 0, 0) # If this were offset by the seed, it would be a potential weakness.
            pixels.append(map_color(r, g, b))
        pixels.append(row_padding(width, 24))

    return pixels

def encode_text_as_image(text_filename, image_filename, seed = "000000", minheight = 4, maxheight = False):

    """ encode_text_as_image(): Encodes ascii text as a bitmap.  Each character is one color (r, g, or b).
            Minimum height of 4 prevents unnecessary padding.
            Seed is used to offset the R, G, B values as a weak layer of security (Correct message 1 in 16,777,216)
            Additional seeds applied (rg, rb, gb, rgb) could mask the seeds but would not provide any additional protection for the message itself since the number of valid values is always 256^3
    """

    with open(text_filename) as text_file:
        text = text_file.read().replace("\n", "")

    ascii = simple_encode(text)
    color_triplets = rgb_triplets(ascii, seed)
    (width, height) = get_dimensions(color_triplets, minheight, maxheight)

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

def decode_image_as_text(image_filename, seed = "000000"):

    (rseed, gseed, bseed) = (int(seed[0:2], base=16), int(seed[2:4], base=16), int(seed[4:6], base=16))

    assert 0 <= rseed <= 255
    assert 0 <= gseed <= 255
    assert 0 <= bseed <= 255

    with open(image_filename, "rb") as decode_file:
        discard_header = decode_file.read(54)

        decoded_text = []

        character_counter = 0
        
        for byte in decode_file.read():

            char = list(struct.unpack("<B", byte)).pop()

            if character_counter == 0:
                rgbseed = bseed
                character_counter = 1
            elif character_counter == 1:
                rgbseed = gseed
                character_counter = 2
            elif character_counter == 2:
                rgbseed = rseed
                character_counter = 0

            if (char - rgbseed) < 0:
                char -= rgbseed
                char += 255
            else:
                char -= rgbseed

            decoded_text.append(chr(char))

    return ''.join(decoded_text)

if __name__ == '__main__':

    try:

        if len(sys.argv) in (4,5,6):
            encode_or_decode = "Encode"
            text_filename = sys.argv[1]
            bitmap_filename = sys.argv[2]
            hexseed = sys.argv[3]
            minimum_height = 4
            maximum_height = False
        elif len(sys.argv) == 3:
            encode_or_decode = "Decode"
            bitmap_filename = sys.argv[1]
            hexseed = sys.argv[2]
        else:
            raise IndexError

        if len(sys.argv) >= 5:
            minimum_height = sys.argv[4] # Optional

        if len(sys.argv) == 6:
            maximum_height = sys.argv[5] # Optional; if there is a conflict, maximum height takes precedence over minimum height
        
    except IndexError:
        print """Parameters for text_to_bitmap.py:
        To Encode Text as a Bitmap: textfile, bitmap_file, secret_hexseed [minimum_height = 4] [maximum_height]
        Example: python text_to_bitmap.py "encodeme.txt" "secret.bmp" afb391

        To Decode a Bitmap into Text: bitmap_file, secret_hexseed
        Example: python text_to_bitmap.py "secret.bmp" afb391"""
        sys.exit(1) 

    if encode_or_decode == 'Encode':
        encode_text_as_image(text_filename, bitmap_filename, hexseed, minimum_height, maximum_height)
    elif encode_or_decode == 'Decode':
        print decode_image_as_text(bitmap_filename, hexseed)
