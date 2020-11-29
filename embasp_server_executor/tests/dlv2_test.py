import logging
import warnings

import tornado
from tornado import web, websocket
from tornado.testing import gen_test

from embasp_server_executor.ese_websocket import ESEWebSocket

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=ResourceWarning)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)


class DLV2Test(tornado.testing.AsyncHTTPTestCase):
    """
    This class tests if the executor interfaces correctly with DLV2.
    """

    def get_app(self):
        # Set up a dummy webserver for the test.
        return web.Application([(r'/', ESEWebSocket)])

    def get_test_url(self):
        return "ws://localhost:" + str(self.get_http_port()) + "/"

    @gen_test
    def test_dlv2_correct_program_and_option(self):
        ws_client = yield websocket.websocket_connect(self.get_test_url())
        program = '["test(0)."]'
        option = '[{"name": "free choice", "value": ["--silent=0"]}]'
        expected_output = r'{"error": "", "model": "{test(0)}\n"}'

        yield ws_client.write_message('{"language" : "asp",' 
                                      '"engine" : "dlv2",' 
                                      '"executor" : "pythonEse",' 
                                      '"program" : %s,' 
                                      '"option" : %s}' % (program, option))

        # Assert if service messages are being sent
        response = yield ws_client.read_message()
        self.assertEqual(response, '{"error": "", "model": "Received command"}')
        response = yield ws_client.read_message()
        self.assertEqual(response, '{"error": "", "model": "Received request for asp, dlv2"}')
        response = yield ws_client.read_message()
        self.assertEqual(response, '{"error": "", "model": "Running..."}')

        # Assert if the actual program output is what we want
        response = yield ws_client.read_message()
        self.assertEqual(response, expected_output)
