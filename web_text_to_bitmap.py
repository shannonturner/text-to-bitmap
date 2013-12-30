#!/usr/local/bin/python2.7

import cherrypy

class Root(object):

    from text_to_bitmap_api import text_to_bitmap_api as text_to_bitmap
    text_to_bitmap.exposed = True

    from text_to_bitmap_api import bitmap_to_text_api as bitmap_to_text
    bitmap_to_text.exposed = True

    from api_front import api_front as api_front
    api_front.exposed = True

    index = api_front
    index.exposed = True
  
if __name__ == '__main__':

    import os.path
    current_dir = os.path.dirname(os.path.abspath(__file__))

    cherrypy.config.update({'server.socket_port': 8080,
                            'server.socket_host': '127.0.0.1',
                            'log.screen': True,
                            'log.error_file': 'site.log'
                            })

    conf = {'/static': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(current_dir, 'static'),
                        }
            }
    
    cherrypy.quickstart(Root(), '/', config=conf)
