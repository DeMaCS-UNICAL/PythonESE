from abc import ABC
from datetime import datetime
from urllib.parse import urlparse

from tornado.websocket import WebSocketHandler

from embasp_server_executor.ese_main import process_program_and_options, cors_origins


class ESEWebSocket(WebSocketHandler, ABC):
    """
    This is the WebSocket handler class. It has been extended to call EmbASP when a message is received.
    """

    # Uncomment this if you want to test out the script on localhost
    def check_origin(self, origin):
        parsed_origin = urlparse(origin)
        # # parsed_origin.netloc.lower() gives localhost:3333
        return parsed_origin.hostname in cors_origins

    def open(self):
        print("\n\n", datetime.now(), "\nWebSocket opened")

    def on_close(self):
        print("WebSocket closed\n\n")

    def on_message(self, message):
        print("Message received: %s" % message)
        process_program_and_options(self, message)
