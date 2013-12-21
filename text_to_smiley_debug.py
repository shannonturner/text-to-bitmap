import struct

def create_rgb_csv(bitmap_filename):

    " Outputs the RGB values for each pixel of the image into debug_rgb_to_csv.csv "

    with open(bitmap_filename, 'rb') as bitmap_file:

        discard_header = bitmap_file.read(54)

        image_width = list(struct.unpack("<B", discard_header[18])).pop() # width is located in discard_header[18] 
            
        values = []

        discard_end_byte = 0

        for byte in bitmap_file.read():
            discard_end_byte += 1
            
            char = list(struct.unpack("<B", byte)).pop()

            if discard_end_byte == (image_width * 3) + 1:
                discard_end_byte = 0
                continue              

            values.append(str(char))

    output = []

    triplet_counter = 0
    column_counter = 0

    for value in values:

        triplet_counter += 1

        output.append(value)

        if triplet_counter == 3:
            output[-5:] = reversed(output[-5:])
            output.append(',')
            column_counter += 1
            triplet_counter = 0
        else:
            output.append(' ')

        if column_counter == image_width:
            output.append('\n')
            column_counter = 0

    output = ''.join(output).split('\n')
    output.reverse()
    output = '\n'.join(output)

    with open("debug_rgb_to_csv.csv", "w") as output_file:
        output_file.write(output.strip())

        return True


if __name__ == '__main__':

    import sys
    create_rgb_csv(sys.argv[1])

