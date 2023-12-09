from asyncio import set_event_loop, new_event_loop
from datetime import datetime
from urllib.parse import urlparse

from tornado.websocket import WebSocketHandler

from ese_config import config as ec
from ese_utils import process_program_and_options, get_output_data


from embasp.base.callback import Callback

class ESEWebSocket(WebSocketHandler, Callback):
    """
    This is the WebSocket handler class. It has been extended to call EmbASP when a message is received.
    """

    # Uncomment this if you want to test out the script on localhost
    def check_origin(self, origin):
        parsed_origin = urlparse(origin)
        # # parsed_origin.netloc.lower() gives localhost:3333
        return parsed_origin.hostname in ec.cors_origins

    def open(self):
        print("\n\n", datetime.now(), "\nWebSocket opened")

    def on_close(self):
        print("WebSocket closed\n\n")

    def on_message(self, message):
        print("Message received: %s" % message)
        process_program_and_options(self, message)

    def callback(self, o):
        o_output, o_errors = "", ""

        if o.get_output() is not None:
            if len(o.get_output()) > ec.max_chars_output:  # Check if the solver output is too long
                o_output = (o.get_output()[:ec.max_chars_output] + "\n[...]\nDo you need more? Let us know")
            else:
                o_output = o.get_output()

        if o.get_errors() is not None:
            if len(o.get_output()) > ec.max_chars_output:  # Check if the solver output is too long
                o_errors = (o.get_errors()[:ec.max_chars_output] + "\n[...]\nDo you need more? Let us know")
            else:
                o_errors = o.get_errors()

        set_event_loop(new_event_loop())
        self.write_message(get_output_data(model=o_output, error=o_errors))
        print("Sent data", get_output_data(model=o_output, error=o_errors))
