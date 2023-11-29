from json import loads, dumps
from re import compile
from sys import platform

from embasp.base.input_program import InputProgram
from embasp.base.option_descriptor import OptionDescriptor
from embasp.platforms.desktop.desktop_handler import DesktopHandler
from embasp.specializations.clingo.desktop.clingo_desktop_service import ClingoDesktopService
from embasp.specializations.dlv.desktop.dlv_desktop_service import DLVDesktopService
from embasp.specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from embasp.specializations.idlv.desktop.idlv_desktop_service import IDLVDesktopService

from ese_config import config as ec


# Check on which OS are we running
system = ""
if platform.startswith("linux"):
    system = "Linux"
elif platform.startswith("win32"):
    system = "Windows"
elif platform.startswith("darwin"):
    system = "macOS"
print("PythonESE starting...")
print("Running on OS:", system)


def add_option(option, handler):
    """
    Function that creates the OptionDescriptor class to be given to the handler
    :param option: the option string to be added
    :param handler: the DesktopHandler instance on which the solver will run
    :return: None
    """
    option_descriptor = OptionDescriptor()
    option_descriptor.add_option(option)
    handler.add_option(option_descriptor)


def check_and_add_options(input_data, handler, engine):
    """
    Function that parses the options received in the client message, checks them,
    and adds them to the EmbASP handler if necessary.

    :param input_data: the message received from the client via the WebSocket
    :param handler: the DesktopHandler class from EmbASP, used to launch the solver process later on
    :param engine: the engine chosen by the client to run the program - different engines have different options
    :return:
    """

    if "option" not in input_data:
        return ""

    options = input_data["option"]

    # Firstly, check if the options we got are available and well-written
    for option in options:
        if "name" in option:
            if option["name"] not in ec.available_options[engine]:
                return "Wrong options"
        else:
            return "Wrong options"

        if "value" in option:
            for value in option["value"]:
                if not compile("[\\w=-]*").match(value):
                    return "Wrong options"

    # Then, if the checks go well, add the options to the DesktopHandler
    for option in options:
        if option["name"] == "":
            continue

        if option["name"] == "free choice":
            if "value" not in option:
                return "Wrong options"
            elif len(option["value"]) > 1:
                # TODO add support for more than 1 free choice value
                return "No more than 1 value supported for 'free choice' at the moment"
            elif option["value"][0] == "":
                return "Error: empty 'free choice' option"
            elif option["value"][0][0] != "-":
                return "Error: 'Free choice' option not valid, it must start with '-'"

        add_option(parse_option_as_string(option), handler)

    return ""

def check_presence_of_parameters(received_message):
    """
    Checks if all the required parameters are present in the received message: engine, language and program.
    :param received_message: the message received from the client, via the websocket, parsed to a json object
    :return: None
    """
    return "engine" in received_message and "language" in received_message and "program" in received_message

def parse_option_as_string(option):
    """
    Function that simply parses the option as a string to be given to the solver executable as argument.
    :param option: option received
    :return: None
    """

    if option["name"] == "free choice":
        return option["value"][0]

    if "value" in option:
        return option["name"] + "".join(option["value"])

    return option["name"]

def process_program_and_options(websocket, message: str):
    """
    Function to be called when the request from the websocket is received.
    This function
    :param websocket: The WebSocket opened by the client (e.g. LoIDE running in a browser)
    :param message: Message received (the program to run and the associated params, such as chosen solver or options
    :return: None
    """
    input_json = message
    websocket.write_message(get_output_data(model="Received command"))
    input_data = loads(input_json)
    print("Message received: %s\n" % input_data)

    if not check_presence_of_parameters(input_data):
        websocket.write_message(get_output_data(error="Wrong parameters"))
        return
    else:
        websocket.write_message(get_output_data(model="Received request for {language}, {engine}"
                                                .format(language=input_data["language"], engine=input_data["engine"])))

    websocket.write_message(get_output_data(model="Running..."))

    engine = input_data["engine"]
    if engine not in ec.paths["executables"]:
        websocket.write_message(get_output_data(
            error="Engine not supported, yet"))
        return

    executable = ec.paths["executables"][engine]

    # If running on a Linux system, use the timeout script
    #if system == "Linux":
    #   exe_path = ec.paths["executables"]["timeout"]
    #else:
    exe_path = str(executable)

    if engine == "dlv":
        service = DLVDesktopService(exe_path)
    elif engine == "clingo":
        service = ClingoDesktopService(exe_path)
    elif engine == "dlv2":
        service = DLV2DesktopService(exe_path)
    elif engine == "idlv":
        service = IDLVDesktopService(exe_path)
    else:
        websocket.write_message(get_output_data(error="Engine not supported, yet"))
        return

    handler = DesktopHandler(service)

#    if system == "Linux":
#        timeout_options = ["-t", ec.limits["time"], "-m", ec.limits["memory"], "--detect-hangups",
#                           "--no-info-on-success"]
#        for o in timeout_options:
#            add_option(o, handler)

    input_program = InputProgram()
    if system == "Windows":
        input_program.add_program(("".join(input_data["program"])).strip())
    else:
        input_program.add_program("".join(input_data["program"]))

    handler.add_program(input_program)

    add_option_check = check_and_add_options(input_data, handler, engine)
    if add_option_check != "":
        websocket.write_message(get_output_data(error=add_option_check))
        return

    # Start the solver process
    handler.start_async(websocket)


def get_output_data(model="", error=""):
    """
    Used to parse as JSON the chosen solver's output+error, so to send it back to the client via the WebSocket.
    :param model: the standard output string from the solver process
    :param error: the standard error string from the solver process
    :return: None
    """
    if error is None:
        error = ""
    return dumps({"model": model, "error": error}, sort_keys=True)

