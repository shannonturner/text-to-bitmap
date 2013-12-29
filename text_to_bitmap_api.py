#!/usr/local/bin/python2.7

def bitmap_to_text_api(self, **kwargs):

    bitmap_filename = kwargs.get('bitmap_filename')
    offset = kwargs.get('offset')
    rgbseed = kwargs.get('rgbseed')
    addvalpos = kwargs.get('addvalpos')
    rgborder = kwargs.get('rgborder')

    import json

    if bitmap_filename is None or offset is None or rgbseed is None or addvalpos is None or rgborder is None:
        return json.dumps("{'error': 'All fields required.'}")

    import requests

    try:
        response = requests.get(bitmap_filename)
    except requests.exception.RequestException:
        return json.dumps("{'error': 'Fetch failed', 'url': '{0}'}".format(bitmap_filename))

    image_to_decode = response.content

    from uni_text_to_bitmap import uni_decode_image_as_text

    instructions = [offset, '{0}'.format(addvalpos), '{0}'.format(rgborder)]

    return json.dumps({'decoded_text': u'{0}'.format(uni_decode_image_as_text(image_to_decode, rgbseed, instructions, as_plaintext=True))})

    

def text_to_bitmap_api(self, **kwargs):

    text_to_encode = kwargs.get('text_to_encode')
    rgbseed = kwargs.get('rgbseed')
    addvalpos = kwargs.get('addvalpos')
    rgborder = kwargs.get('rgborder')

    import hashlib
    import json
    import time
    from uni_text_to_bitmap import uni_encode_text_as_image

    if text_to_encode is None:
        return json.dumps("{'error': 'Text to encode is a required field.'}")

    if rgbseed is None:
        from text_to_bitmap_autogen import generate_hexseed
        rgbseed = ''.join(list(generate_hexseed(1))) # When issue #3 is resolved, you can change this to allow more seeds similar to text_to_bitmap_autogen.create_instructions()

    if addvalpos is None:
        import random
        from text_to_bitmap_autogen import generate_addvalpos
        addvalpos = ''.join(list(generate_addvalpos(random.randint(4, 24))))

    if rgborder is None:
        import random
        from text_to_bitmap_autogen import generate_rgbscrambling
        rgborder = ','.join(list(generate_rgbscrambling(random.randint(4, 12))))

    unique_id = hashlib.sha256('{0}{1}'.format(''.join([str(time_chunk) for time_chunk in time.localtime()[:6]]), random.randint(1,100))).hexdigest()[:10]
    bitmap_filename = 'temp_bmp_{0}-{1}.bmp'.format(''.join([str(time_chunk) for time_chunk in time.localtime()[:6]]), unique_id)
    
    offset = uni_encode_text_as_image(text_to_encode, bitmap_filename, rgbseed, [addvalpos, rgborder], as_plaintext = True)

    return json.dumps({'offset': offset,
                       'rgbseed': rgbseed,
                       'addvalpos': addvalpos,
                       'rgb_order': rgborder,
                       'file_url': bitmap_filename
                       })
