# region imports
import cherrypy
import atexit
import sys

from globals import *

from rest import Root
from rest import Methods
from rest import ExitCherryPyServer
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
        console_log(error_message, LOG_ERROR, main.__name__)
        return False


@atexit.register
def at_exit_file():
    console_log('The cherrypy server has been exited.')
    cherrypy.engine.stop()
    sys.exit(0)


if __name__ == "__main__":
    main()
# endregion main
