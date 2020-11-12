import logging
import warnings

import tornado
from tornado import web, websocket
from tornado.testing import gen_test

from embasp_server_executor.ese_websocket import ESEWebSocket

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=ResourceWarning)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)

clingo_version = "5.4.0"

class ClingoTest(tornado.testing.AsyncHTTPTestCase):

    """
    This class tests if the executor interfaces correctly with Clingo. Change version as needed.
    """

    def get_app(self):
        # Set up a dummy webserver for the test.
        return web.Application([(r'/', ESEWebSocket)])

    def get_test_url(self):
        return "ws://localhost:" + str(self.get_http_port()) + "/"

    @gen_test
    def test_clingo_correct_program_and_option(self):
        ws_client = yield websocket.websocket_connect(self.get_test_url())
        program = '["test(0)."]'
        option = '[{"name": ""}]'
        expected_output = r'{"error": "", "model": "clingo version %s\nReading from stdin\nSolving...\nAnswer: ' \
                          r'1\ntest(0)\nSATISFIABLE\n\nModels       : 1\nCalls        : 1\nTime         : 0.000s (' \
                          r'Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)\nCPU Time     : 0.000s\n"}' % clingo_version

        yield ws_client.write_message('{"language" : "asp",' 
                                      '"engine" : "clingo",' 
                                      '"executor" : "pythonEse",' 
                                      '"program" : %s,' 
                                      '"option" : %s}' % (program, option))


        # Assert if service messages are being sent
        response = yield ws_client.read_message()
        self.assertEqual(response, '{"error": "", "model": "Received command"}')
        response = yield ws_client.read_message()
        self.assertEqual(response, '{"error": "", "model": "Received request for asp, clingo"}')
        response = yield ws_client.read_message()
        self.assertEqual(response, '{"error": "", "model": "Running..."}')

        # Assert if the actual program output is what we want
        response = yield ws_client.read_message()
        self.assertEqual(response, expected_output)
