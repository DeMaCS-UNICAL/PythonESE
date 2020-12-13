#!/usr/bin/env python

# import asyncio
from os import path

from tornado.ioloop import IOLoop
# from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from tornado.web import Application

from embasp_server_executor.ese_config import config as ec
from embasp_server_executor.ese_websocket import ESEWebSocket

def make_app():
    """
    Creates an instance of the WebSocket handler.
    :return: None
    """
    print("Starting web Application")
    return Application([(r"/", ESEWebSocket)])


if __name__ == "__main__":
    ec.read_config_file()

    app = make_app()
    # app.listen(8765)
    # TODO find a better way to do this
    if path.isfile(ec.paths["certificate"]["cert_file"]) and path.isfile(ec.paths["certificate"]["key_file"]):
        app.listen(ec.port_number, ssl_options={
            "certfile": ec.paths["certificate"]["cert_file"],
            "keyfile": ec.paths["certificate"]["key_file"],
        })
    else:
        app.listen(ec.port_number)

    # asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
    IOLoop.current().start()
