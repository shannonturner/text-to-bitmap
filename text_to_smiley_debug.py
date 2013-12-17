import struct

def create_csv(bitmap_filename):

    " Outputs the RGB values for each pixel of the smiley into text_to_smiley.csv "

    with open(bitmap_filename, 'rb') as bitmap_file:

        discard_header = bitmap_file.read(54)

        values = []

        discard_end_byte = 0

        for byte in bitmap_file.read():
            discard_end_byte += 1
            
            char = list(struct.unpack("<B", byte)).pop()

            if discard_end_byte == 40: # (13 pixels * r,g,b) + 1 = end byte to discard
                discard_end_byte = 0
                continue              

            values.append(str(char))

    output = []

    triplet_counter = 0
    column_counter = 0

    for value in reversed(values):

        triplet_counter += 1

        output.append(value)

        if triplet_counter == 3:
            output.append(',')
            column_counter += 1
            triplet_counter = 0
        else:
            output.append(' ')

        if column_counter == 13:
            output.append('\n')
            column_counter = 0

    with open("text_to_smiley.csv", "w") as output_file:
        output_file.write(''.join(output))

        return True


if __name__ == '__main__':

    import sys
    create_csv(sys.argv[1])
