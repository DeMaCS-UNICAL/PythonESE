from base.callback import Callback

from embasp_server_executor.src.ese_main import max_chars_output, get_output_data


class ESECallback(Callback):
    """
    The ESECallback class extends EmbASP's Callback class.
    It is used to launch the chosen solver process (depending on the type of DesktopService used),
    fetch the output, and write a message to the WebSocket.
    """

    def __init__(self, websocket):
        self._websocket = websocket

    def callback(self, o):
        o_output, o_errors = "", ""

        if o.get_output() is not None:
            if len(o.get_output()) > max_chars_output:  # Check if the solver output is too long
                o_output = (o.get_output()[:max_chars_output] + "\n[...]\nDo you need more? Let us know")
            else:
                o_output = o.get_output()

        if o.get_errors() is not None:
            if len(o.get_output()) > max_chars_output:  # Check if the solver output is too long
                o_errors = (o.get_errors()[:max_chars_output] + "\n[...]\nDo you need more? Let us know")
            else:
                o_errors = o.get_errors()

        self._websocket.write_message(get_output_data(model=o_output, error=o_errors))
        print("Sent data", get_output_data(model=o_output, error=o_errors))
