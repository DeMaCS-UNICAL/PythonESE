#!/usr/bin/env python

import asyncio
import json
# import os
import re
import sys
from configparser import ConfigParser

from tornado.ioloop import IOLoop
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from tornado.web import Application
from tornado.websocket import WebSocketHandler

from embasp.base.callback import Callback
from embasp.base.input_program import InputProgram
from embasp.base.option_descriptor import OptionDescriptor
from embasp.platforms.desktop.desktop_handler import DesktopHandler
from embasp.specializations.clingo.desktop.clingo_desktop_service import ClingoDesktopService
from embasp.specializations.dlv.desktop.dlv_desktop_service import DLVDesktopService
from embasp.specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService


p = re.compile("[\\w=-]*")

executables = {}

options_dict = {
    "dlv": ["", "free choice", "-silent", "-filter=", "-nofacts", "-FC"],
    "clingo": ["", "free choice"],
    "dlv2": ["", "free choice", "-silent", "-filter="]
}

system = ""
if sys.platform.startswith("linux"):
    system = "Linux"
elif sys.platform.startswith("win32"):
    system = "Windows"
elif sys.platform.startswith("darwin"):
    system = "macOS"
print("system is:", system)


class MyCallback(Callback):
    def __init__(self, websocket):
        print("Created callback")
        self._websocket = websocket

    def callback(self, o):
        # print("callback called", o.get_output(), o.get_errors())
        # self.websocket.send(get_output_data(
        #     model=o.get_output(), error=o.get_errors()))
        o_output, o_errors = "", ""
        if o.get_output() is not None:
            o_output = (o.get_output()[:max_chars_output] + "\n[...]\nDo you need more? Let us know") if len(
                o.get_output()) > max_chars_output else o.get_output()
        if o.get_errors() is not None:
            o_errors = (o.get_errors()[:max_chars_output] + "\n[...]\nDo you need more? Let us know") if len(
                o.get_errors()) > max_chars_output else o.get_errors()
        self._websocket.write_message(
            get_output_data(model=o_output, error=o_errors))
        print("Sent data", get_output_data(
            model=o_output, error=o_errors))


def check_required_data(input_data):
    return "engine" in input_data and "language" in input_data and "program" in input_data


def get_output_data(model="", error=""):
    if error is None:
        error = ""
    return json.dumps({"model": model, "error": error})


def check_options(options, engine):
    for option in options:
        if "name" in option:
            if option["name"] not in options_dict[engine]:
                return False
        else:
            return False

        if "value" in option:
            for value in option["value"]:
                if not p.match(value):
                    return False

    return True


def get_option(option, engine):
    # print(option["name"])

    if option["name"] == "free choice":
        return option["value"][0]

    if "value" in option:
        return option["name"] + "".join(option["value"])

    return option["name"]


def add_option(option, handler):
    option_descriptor = OptionDescriptor()
    option_descriptor.add_option(option)
    handler.add_option(option_descriptor)


def add_options(options, handler):
    [add_option(option, handler) for option in options]


def check_and_add_options(input_data, handler, engine):
    if "option" not in input_data:
        return ""

    options = input_data["option"]
    # print(options)

    if not check_options(options, engine):
        return "Wrong options"

    # if len(options) > 1:
    #     return "No more than 1 named option supported at the moment"

    for option in options:
        if option["name"] == "":
            continue

        if option["name"] == "free choice":
            if "value" not in option:
                return "Wrong options"
            elif len(option["value"]) > 1:
                return "No more than 1 value supported for 'free choice' at the moment"
            elif option["value"][0] == "":
                return "Error: empty 'free choice' option"
            elif option["value"][0][0] != "-":
                return "Error: 'Free choice' option not valid, it must start with '-'"

        add_option(get_option(option, engine), handler)

    if engine == "clingo":
        add_option("--", handler)

    return ""


def run_engine_tornado(websocket, message):
    input_json = message
    # print(f"< {input_data}")
    websocket.write_message(get_output_data(model="Received command"))

    input_data = json.loads(input_json)
    print(input_data)

    if not check_required_data(input_data):
        websocket.write_message(get_output_data(error="Wrong parameters"))
        return
    else:
        websocket.write_message(get_output_data(model="Received request for {language}, {engine}".format(
            language=input_data["language"], engine=input_data["engine"])))

    websocket.write_message(get_output_data(model="Running..."))

    engine = input_data["engine"]
    if engine not in executables:
        websocket.write_message(get_output_data(
            error="Engine not supported, yet"))
        return

    executable = executables[engine]

    if system == "Linux":
        exe_path = executables["timeout"]
    else:
        exe_path = executable

    if engine == "dlv":
        service = DLVDesktopService(exe_path)
    elif engine == "clingo":
        service = ClingoDesktopService(exe_path)
    elif engine == "dlv2":
        service = DLV2DesktopService(exe_path)
    else:
        websocket.write_message(get_output_data(
            error="Engine not supported, yet"))
        return

    handler = DesktopHandler(service)

    if system == "Linux":
        add_option(["-t", "20", "-m", "200000", "--detect-hangups",
                    "--no-info-on-success", executable], handler)

    # program = "".join(input_data["program"])
    # print(program)

    inp = InputProgram()
    if system == "Windows":
        inp.add_program(("".join(input_data["program"])).strip())
    else:
        inp.add_program("".join(input_data["program"]))

    handler.add_program(inp)

    addopt_ret = check_and_add_options(input_data, handler, engine)
    if addopt_ret != "":
        websocket.write_message(get_output_data(error=addopt_ret))
        return

    mc = MyCallback(websocket)
    handler.start_async(mc)

    # output_engine = handler.start_sync()
    # websocket.write_message(get_output_data(model=output_engine.get_output(), error=output_engine.get_errors()))


class ESEWebSocket(WebSocketHandler):
    # CORS_ORIGINS = ["localhost"]

    # def check_origin(self, origin):
    #     parsed_origin = urlparse(origin)
    #     # parsed_origin.netloc.lower() gives localhost:3333
    #     return parsed_origin.hostname in self.CORS_ORIGINS

    def open(self):
        print("\n\nWebSocket opened")

    def on_close(self):
        print("WebSocket closed\n\n")

    def on_message(self, message):
        # self.write_message(u"You said: " + message)
        run_engine_tornado(self, message)


def make_app():
    print("Starting web Application")
    return Application([
        (r"/", ESEWebSocket)
    ])


def read_config_file():
    global executables
    global max_chars_output

    config = ConfigParser()

    # default values
    config.read_dict({
        "executables": {
            "dlv": "executables/dlv/dlv",
            "clingo": "executables/clingo/clingo",
            "dlv2": "executables/dlv2/dlv2",
            "timeout": "executables/timeout/timeout"},
        "output": {
            "max_chars": 10000
        }
    })

    config.read("config.ini")

    for key in config["executables"]:
        executables[key] = config["executables"][key]
        print(key, "path set to:", executables[key])

    max_chars_output = config.getint("output", "max_chars")
    print("max_chars_output is:", max_chars_output)


if __name__ == "__main__":
    read_config_file()
    # asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
    app = make_app()
    app.listen(8765)
    IOLoop.instance().start()
