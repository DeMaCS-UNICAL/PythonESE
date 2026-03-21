#!/usr/bin/env python

# import asyncio
import signal
import sys
from os import path

from tornado.ioloop import IOLoop
# from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from tornado.web import Application

from .ese_config import config as ec
from .ese_websocket import ESEWebSocket


def make_app():
    """
    Creates an instance of the WebSocket handler.
    :return: None
    """
    print("Starting web Application")
    return Application([(r"/", ESEWebSocket)])


def signal_handler(signum, frame):
    try:
        signal_name = signal.Signals(signum).name
    except ValueError:
        signal_name = f"UNKNOWN({signum})"
    print(f"\nReceived signal {signal_name}. Shutting down...")
    IOLoop.current().stop()


def main() -> int:
    # Register signal handlers for graceful shutdown
    for sig in (signal.SIGTERM, signal.SIGINT): # signal.SIGTSTP
        signal.signal(sig, signal_handler)
    
    try:
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
        # Start the IOLoop (blocks until stop() is called)
        IOLoop.current().start()

    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        return 1

    # Reached after IOLoop.stop() (e.g., on SIGTERM/SIGINT)
    print("Server stopped.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
