#!/usr/local/bin/python2.7

def api_front(self, **kwargs):

    action = kwargs.get('action')

    bitmap_filename = kwargs.get('bitmap_filename')
    offset = kwargs.get('offset')
    rgbseed = kwargs.get('rgbseed')
    addvalpos = kwargs.get('addvalpos')
    rgborder = kwargs.get('rgborder')
    password = kwargs.get('password')

    text_to_encode = kwargs.get('text_to_encode')

    page_source = []

    if action == 'encode' and text_to_encode is not None:
        import requests
        import urllib

        param_string = '?text_to_encode={0}'.format(urllib.unquote(text_to_encode))

        if rgbseed is not None:
            param_string = "{0}&rgbseed={1}".format(param_string, rgbseed)

        if addvalpos is not None:
            param_string = "{0}&addvalpos={1}".format(param_string, addvalpos)

        if rgborder is not None:
            param_string = "{0}&rgborder={1}".format(param_string, rgborder)

        if password is not None:
            param_string = "{0}&password={1}".format(param_string, password)
        
        response = requests.get('http://shannonvturner.com/t2b/text_to_bitmap{0}'.format(param_string)).json()

        if response.get('error') is None:
            page_source.append('<h3>Your text has been successfully encoded!</h3>')

            page_source.append('Image Download: <a href="./{0}" target="_blank">Download your image</a>'.format(response['file_url']))
            page_source.append('<a href="./{0}" target="_blank"><img src="./{0}"></a>'.format(response['file_url']))

            page_source.append('<br><b>For your intended recipient to be able to decode the message properly, they will need these SECRET INSTRUCTIONS</b><br>')

            page_source.append('<br>Password: <b>{0}</b> <br><i>OR: </i><br>'.format(response['password']))

            page_source.append('<ul><li>Addition Value Position Ordering: {0}</li>'.format(response['addvalpos']))
            page_source.append('<li>RGB Ordering: {0}</li>'.format(response['rgborder']))
            page_source.append('<li>RGB Seed: {0}</li>'.format(response['rgbseed']))
            page_source.append('<li>Offset: {0}</li></ul>'.format(response['offset']))

    elif action == 'decode' and bitmap_filename is not None and ((offset is not None and rgbseed is not None and addvalpos is not None and rgborder is not None) or password is not None):
        
        import requests

        if password is not None:
            param_string = '?bitmap_filename={0}&password={1}'.format(bitmap_filename, password)
        else:
            param_string = '?bitmap_filename={0}&offset={1}&rgbseed={2}&addvalpos={3}&rgborder={4}'.format(bitmap_filename, offset, rgbseed, addvalpos, rgborder)

        response = requests.get('http://shannonvturner.com/t2b/bitmap_to_text{0}'.format(param_string)).json()

        if response.get('error') is None:

            if response.get('decode_error') is None:
                try:
                    page_source.append('<h3>Your image was successfully decoded!</h3><br>Message:<hr><br>{0}<hr>'.format(response['decoded_text']))
                except Exception:
                    page_source.append('<h3>Failed to decode.</h3><br><b>Are you sure your decoding instructions are correct?</b><br>')
            else:
                page_source.append('<h3>Failed to decode.</h3><br><b>Are you sure your decoding instructions are correct?</b><br>')

    with open('t2bapi_front_footer.html', 'r') as footer_file:
        page_source.append(footer_file.read())

    return page_source
