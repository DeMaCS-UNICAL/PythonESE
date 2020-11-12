from abc import ABC
from datetime import datetime

from tornado.websocket import WebSocketHandler

from embasp_server_executor.ese_main import process_program_and_options


class ESEWebSocket(WebSocketHandler, ABC):
    """
    This is the WebSocket handler class. It has been extended to call EmbASP when a message is received.
    """

    # Uncomment this if you want to test out the script on localhost
    # def check_origin(self, origin):
    #     parsed_origin = urlparse(origin)
    #     return parsed_origin.hostname in self.CORS_ORIGINS

    def open(self):
        print("\n\n", datetime.now(), "\nWebSocket opened")

    def on_close(self):
        print("WebSocket closed\n\n")

    def on_message(self, message):
        process_program_and_options(self, message)
