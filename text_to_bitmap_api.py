#!/usr/local/bin/python2.7

def bitmap_to_text_api(self, **kwargs):

    bitmap_filename = kwargs.get('bitmap_filename')
    offset = kwargs.get('offset')
    rgbseed = kwargs.get('rgbseed')
    addvalpos = kwargs.get('addvalpos')
    rgborder = kwargs.get('rgborder')

    import json

    if bitmap_filename is None or offset is None or rgbseed is None or addvalpos is None or rgborder is None:
        return json.dumps({'error': 'All fields (bitmap_filename, offset, rgbseed, addvalpos, rgborder) required.'})

    import requests

    try:
        response = requests.get(bitmap_filename)
    except requests.exception.RequestException:
        return json.dumps({'error': 'Fetch failed', 'url': '{0}'}.format(bitmap_filename))

    image_to_decode = response.content

    from uni_text_to_bitmap import uni_decode_image_as_text

    instructions = [int(offset), '{0}'.format(addvalpos), '{0}'.format(rgborder)]

    try:
        return json.dumps({'decoded_text': u'{0}'.format(uni_decode_image_as_text(image_to_decode, rgbseed, instructions, as_plaintext=True))})
    except Exception:
        return json.dumps({'decode_error': 'Failed to decode.  Are you sure your decoding instructions are correct?'})

    

def text_to_bitmap_api(self, **kwargs):

    text_to_encode = kwargs.get('text_to_encode')
    rgbseed = kwargs.get('rgbseed')
    addvalpos = kwargs.get('addvalpos')
    rgborder = kwargs.get('rgborder')

    import hashlib
    import json
    import random
    import time
    from uni_text_to_bitmap import uni_encode_text_as_image

    if text_to_encode is None:
        return json.dumps({'error': 'text_to_encode is a required field.'})

    if rgbseed is None:
        from text_to_bitmap_autogen import generate_hexseed
        rgbseed = ''.join(list(generate_hexseed(1))) # When issue #3 is resolved, you can change this to allow more seeds similar to text_to_bitmap_autogen.create_instructions()

    if addvalpos is None:
        from text_to_bitmap_autogen import generate_addvalpos
        addvalpos = ''.join(list(generate_addvalpos(random.randint(4, 24))))

    if rgborder is None:
        from text_to_bitmap_autogen import generate_rgbscrambling
        rgborder = ','.join(list(generate_rgbscrambling(random.randint(4, 12))))

    unique_id = hashlib.sha256('{0}{1}'.format(''.join([str(time_chunk) for time_chunk in time.localtime()[:6]]), random.randint(1,100))).hexdigest()[:10]
    bitmap_filename = 'temp_bmp_{0}-{1}.bmp'.format(''.join([str(time_chunk) for time_chunk in time.localtime()[:6]]), unique_id)
    
    offset = uni_encode_text_as_image(text_to_encode, bitmap_filename, rgbseed, [addvalpos, rgborder], as_plaintext = True)

    return json.dumps({'offset': offset,
                       'rgbseed': rgbseed,
                       'addvalpos': addvalpos,
                       'rgborder': rgborder,
                       'file_url': bitmap_filename
                       })


def text_to_smiley_api(self, **kwargs):

    text_to_encode = kwargs.get('text_to_encode')
    
    if text_to_encode is None:
        return json.dumps({'error': 'text_to_encode is a required field.'})

    import hashlib
    import random
    import time

    unique_id = hashlib.sha256('{0}{1}'.format(''.join([str(time_chunk) for time_chunk in time.localtime()[:6]]), random.randint(1,100))).hexdigest()[:10]
    bitmap_filename = 's_{0}-{1}.bmp'.format(''.join([str(time_chunk) for time_chunk in time.localtime()[:6]]), unique_id)
   
    return_message = {}

    if len(text_to_encode) > 84:
        return_message['length_warning'] = 'Only messages of 84 or fewer characters may be entered.  Message will be truncated.'

    alter_base('base_smiley.bmp', bitmap_filename, text_to_encode)

    return_message['bitmap_filename'] = bitmap_filename

    return json.dumps(return_message)


