# region imports
from unittest import loader

import cherrypy
import sys

from globals import *
# endregion imports


# region Methods
class Root(object):
    @cherrypy.expose
    def index(self):
        tmpl = open('index.html')
        return tmpl


@cherrypy.expose
class Methods(object):
    @cherrypy.tools.json_out()
    def GET(self):
        # return cherrypy.session['mystring']
        return {
            'GET message': 'Hello World'
        }

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self, length=8):
        return {
            'POST message': 'Hello World'
        }

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self):
        return {
            'PUT message': 'Hello World'
        }

    @cherrypy.tools.json_out()
    def DELETE(self):
        return {
            'DELETE message': 'Hello World'
        }


@cherrypy.expose
class ExitCherryPyServer(object):
    @cherrypy.tools.json_out()
    def GET(self):
        cherrypy.engine.exit()
        return {
            'EXIT message': 'Hello World',
            'exit': sys.exit(0)
        }
# endregion Methods

