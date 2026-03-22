import json
import os

# TODO implement in a better way

class Config:

    # Instantiate globally some variables that will be used across multiple functions in the script
    paths = {"executables": {}, "certificate": {}}
    execution_limits = {}
    available_options = {}
    cors_origins = []
    port_number = None
    max_chars_output = None
    execution_variants = {}

    def __init__(self) -> None:
        super().__init__()
        self.read_config_file()

    def read_config_file(self):
        """
        Reads the config json and fills objects used by the script.
        :return: None
        """

        with open(os.path.join("config_files", "config.json"), 'r') as file:
            config = json.load(file)

            for key in config["paths"]["executables"]:
                self.paths["executables"][key] = str(config["paths"]["executables"][key])
                print(key, "path set to:", self.paths["executables"][key])

            for key in config["available_options"]:
                self.available_options[key] = config["available_options"][key]

            self.paths["certificate"]["cert_file"] = config["paths"]["certificate"]["cert_file"]
            self.paths["certificate"]["key_file"] = config["paths"]["certificate"]["key_file"]
            self.port_number = config["server_properties"]["port_number"]
            self.cors_origins = config["server_properties"]["cors_origins"]

            self.max_chars_output = int(config["execution_output"]["max_chars"])
            print("max_chars_output is:", self.max_chars_output)

            for key in config["execution_limits"]:
                self.execution_limits[key] = int(config["execution_limits"][key])
                print(key, "limit set to:", self.execution_limits[key])

            for key in config["execution_variants"]:
                self.execution_variants[key] = bool(config["execution_variants"][key])
                print(key, "execution method set to:", self.execution_variants[key])

config = Config()
