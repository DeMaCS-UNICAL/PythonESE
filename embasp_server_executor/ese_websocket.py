from asyncio import new_event_loop, set_event_loop
from datetime import datetime
from urllib.parse import urlparse

from embasp.base.callback import Callback
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

from .ese_config import config as ec
from .ese_utils import get_output_data, process_program_and_options


class ESEWebSocket(WebSocketHandler, Callback):
    """
    This is the WebSocket handler class. It has been extended to call EmbASP when a message is received.
    """

    io_loop: IOLoop = None

    def check_origin(self, origin):
        parsed_origin = urlparse(origin)
        return parsed_origin.hostname in ec.cors_origins

    def open(self):
        # Capture the *current* IOLoop instance - this is the one running the WebSocket
        self.io_loop = IOLoop.current()
        print("\n\n", datetime.now(), "\nWebSocket opened")

    def on_close(self):
        print("WebSocket closed\n\n")

    def on_message(self, message):
        print("Message received: %s" % message)
        process_program_and_options(self, message)

    def callback(self, o):
        o_output, o_errors = "", ""

        if o.get_output() is not None:
            # Check if the solver output is too long
            if len(o.get_output()) > ec.max_chars_output:
                o_output = (o.get_output()[:ec.max_chars_output] + "\n[...]\nDo you need more? Let us know")
            else:
                o_output = o.get_output()

        if o.get_errors() is not None:
            # Check if the solver error is too long
            if len(o.get_errors()) > ec.max_chars_output:
                o_errors = (o.get_errors()[:ec.max_chars_output] + "\n[...]\nDo you need more? Let us know")
            else:
                o_errors = o.get_errors()

        # Use the stored loop
        if self.io_loop is None:
            print("Callback called before WebSocket opened!", file=sys.stderr)
            return

        self.io_loop.add_callback(self._write_result, o_output, o_errors)

    def _write_result(self, model: str, error: str):
        try:
            data = get_output_data(model=model, error=error)
            self.write_message(data)
            print("Sent data", data)
        except Exception as e:
            print(f"Failed to write message: {e}", file=sys.stderr)
