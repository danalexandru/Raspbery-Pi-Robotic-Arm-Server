# region imports
import cherrypy
import logging

from globals import *
# endregion imports


# region Methods
@cherrypy.expose
class Methods(object):
    @cherrypy.tools.accept(media='text/plain')
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
class ExitCherrypyServer(object):
    def GET(self):
        cherrypy.engine.exit()
        return {
            'EXIT message': 'Hello World'
        }

# endregion Methods 


# region main
def main():
    try:
        cherrypy.engine.exit()

        conf = {
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
        }

        cherrypy.config.update({
            #'server.socket_host': '127.0.0.1',
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 9090
            })

        cherrypy.tree.mount(Methods(), '/api/tools', conf)
        cherrypy.tree.mount(ExitCherrypyServer(), '/api/exit', conf)

        cherrypy.engine.start()
        cherrypy.engine.block()

    except Exception as error_message:
        console_log(error_message, LOG_ERROR, main.__name__)
        return False


if __name__== "__main__":
    main()
# endregion main

