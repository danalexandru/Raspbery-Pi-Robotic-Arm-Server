"""
This file is the main part of the Project. This is the file that is being executed at the start of the cherrypy server
"""


# region imports
import cherrypy
import atexit
import sys

from globals import console

from rest import Root, Methods, ExitCherryPyServer
# endregion imports


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
            # 'server.socket_host': '127.0.0.1',
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 9090
        })

        cherrypy.tree.mount(Root(), '/')
        cherrypy.tree.mount(Methods(), '/api/tools', conf)
        cherrypy.tree.mount(ExitCherryPyServer(), '/api/exit', conf)

        cherrypy.engine.start()
        cherrypy.engine.block()

    except Exception as error_message:
        console.log(error_message, console.LOG_ERROR, main.__name__)
        return False


@atexit.register
def at_exit_file():
    console.log('The cherrypy server has been shut down.', console.LOG_SUCCESS, at_exit_file.__name__)
    cherrypy.engine.stop()
    cherrypy.engine.exit()


if __name__ == '__main__':
    main()
# endregion main
