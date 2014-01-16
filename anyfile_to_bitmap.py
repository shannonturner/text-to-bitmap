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

        anyfile.write(''.join(write_this))


def anyfile_to_bitmap(**kwargs):

    " Convert any file to a bitmap "

    filename = kwargs.get('filename')
    char_offset = kwargs.get('char_offset')
    original_extension = kwargs.get('original_extension')

    if filename is None:
        return "filename is a required parameter for anyfile_to_bitmap()"

    if char_offset is None:
        import random
        char_offset = random.randint(0, 65280)
    else:
        assert 0 <= char_offset <= 65280

    data = anyfile_to_bytes(filename)
    kwargs['text_to_encode'] = ''.join(bytes_to_text(data, char_offset))

    import json
    import text_to_bitmap_api

    json_return = json.loads(text_to_bitmap_api.text_to_bitmap_api(0, **kwargs))

    json_return['char_offset'] = char_offset
    json_return['original_extension'] = original_extension

    return json_return
    

def bitmap_to_anyfile(**kwargs):

    " Convert a specially-encoded bitmap to any type of file. "

    bitmap_filename = kwargs.get('file_url')
    char_offset = kwargs.get('char_offset')
    original_extension = kwargs.get('original_extension')
    password = kwargs.get('password')

    from uni_text_to_bitmap import uni_decode_image_as_text

    try:
        offset, rgbseed, addvalpos, rgborder = kwargs.get('password').split('_')
    except Exception:
        return "[ERROR] Password is a required field."

    instructions = [int(offset), '{0}'.format(addvalpos), '{0}'.format(rgborder)]

    try:
        decoded_text = u'{0}'.format(uni_decode_image_as_text(bitmap_filename, rgbseed, instructions))
    except Exception, e:
        return "[FAILED] Failed to decode. Are you sure your decoding instructions are correct? {0} Error code: {1}".format(password, e)

    import hashlib

    data = text_to_bytes(decoded_text, char_offset)
    unique_id = hashlib.sha256(''.join([str(c) for c in data])).hexdigest()[:10]
    bytes_to_anyfile(data, '{0}.{1}'.format(unique_id, original_extension))

    return "File created: '{0}.{1}'".format(unique_id, original_extension)
    
