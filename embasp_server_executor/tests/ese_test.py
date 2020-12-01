import logging
import warnings

import tornado
from tornado import web, websocket
from tornado.testing import gen_test

from embasp_server_executor.src.ese_websocket import ESEWebSocket

warnings.filterwarnings("ignore", category=RuntimeWarning)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)


def build_dummy_model(option):
    return '{"language" : "asp",' \
           '"engine" : "dlv2",' \
           '"executor" : "pythonEse",' \
           '"program" : [],' \
           '"option" : %s}' % option


class ESETest(tornado.testing.AsyncHTTPTestCase):
    """
    This class test the processing of the input data from the client before it is sent to the solver process
    for execution.
    Notice how we build a "dummy" input model that contains an empty program, as it will not
    be executed at all.
    It's not the purpose of the class: all test stop before sending the input to the solver.
    """

    def get_app(self):
        # Set up a dummy webserver for the test.
        return web.Application([(r'/', ESEWebSocket)])

    def get_test_url(self):
        return "ws://localhost:" + str(self.get_http_port()) + "/"

    @gen_test
    def test_wrong_option(self):
        ws_client = yield websocket.websocket_connect(self.get_test_url())
        option = '[{"name" : "unsupported"}]'  # Here we add an unsupported option.
        expected_output = r'{"error": "Wrong options", "model": ""}'

        yield ws_client.write_message(build_dummy_model(option))

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

    @gen_test
    def test_more_than_one_free_choice(self):
        ws_client = yield websocket.websocket_connect(self.get_test_url())
        option = '[{"name": "free choice", "value": ["--t", "--no-facts"]}]'
        expected_output = '{"error": "No more than 1 value supported for \'free choice\' at the moment", "model": ""}'

        yield ws_client.write_message(build_dummy_model(option))

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

    @gen_test
    def test_invalid_free_choice(self):
        ws_client = yield websocket.websocket_connect(self.get_test_url())
        option = '[{"name": "free choice", "value": ["t"]}]'
        expected_output = '{"error": "Error: \'Free choice\' option not valid, it must start with \'-\'", "model": ""}'

        yield ws_client.write_message(build_dummy_model(option))

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

    @gen_test
    def test_empty_free_choice(self):
        ws_client = yield websocket.websocket_connect(self.get_test_url())
        option = '[{"name": "free choice", "value": [""]}]'
        expected_output = '{"error": "Error: empty \'free choice\' option", "model": ""}'

        yield ws_client.write_message(build_dummy_model(option))

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

    @gen_test
    def test_wrong_parameters(self):
        ws_client = yield websocket.websocket_connect(self.get_test_url())
        expected_output = r'{"error": "Wrong parameters", "model": ""}'

        yield ws_client.write_message('{"language" : "asp"}')  # Send a request with missing parameters

        # Assert if service messages are being sent
        response = yield ws_client.read_message()
        self.assertEqual(response, '{"error": "", "model": "Received command"}')
        response = yield ws_client.read_message()
        self.assertEqual(response, expected_output)
