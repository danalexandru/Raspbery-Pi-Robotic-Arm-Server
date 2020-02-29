"""
Description: This file has the REST API functionality
"""

# region imports
from unittest import loader

import cherrypy
import sys

from obs import methods_handler
from globals import console, rest_error_message_handler
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
    def POST(self):
        try:
            input_json = cherrypy.request.json

            if methods_handler.interpret_json(input_json) is True:
                return True
            else:
                raise cherrypy.HTTPError(400, rest_error_message_handler.get_last_error_message())

        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            raise cherrypy.HTTPError(400, str(rest_error_message_handler.get_last_error_message()))

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self):
        return {
            'PUT message': 'Hello World'
        }

    @cherrypy.tools.json_out()
    def DELETE(self):
        raise cherrypy.HTTPError(400, 'Hello World')


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
