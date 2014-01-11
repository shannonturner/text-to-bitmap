import struct

def bytes_to_text(tuples, char_offset=0):

    assert 0 <= char_offset <= 65280 # 65535 - 255

    text = []

    for number in tuples:
        text.append(unichr(char_offset + number[0]))

    return text


def text_to_bytes(text, char_offset=0):

    assert 0 <= char_offset <= 65280 # 65535 - 255

    tuples = []

    for char in text:
        tuples.append((abs(char_offset - ord(char)), ))

    return tuples


def anyfile_to_bytes(filename):

    data = []

    with open(filename, 'rb') as anyfile:
        for byte in anyfile.read():
            data.append(struct.unpack("<B", byte))

    return data

def bytes_to_anyfile(data, filename):

    write_this = []

    with open(filename, 'wb') as anyfile:
        for byte in data:
            write_this.append(struct.pack("<B", byte[0]))

    anyfile.write(write_this)
