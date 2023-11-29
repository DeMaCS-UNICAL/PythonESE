import json
import os

# TODO implement in a better way

class Config:

    # Instantiate globally some variables that will be used across multiple functions in the script
    paths = {"executables": {}, "certificate": {}}
    limits = {}
    available_options = {}
    cors_origins = []
    port_number = None
    max_chars_output = None

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
                self.paths["executables"][key] = config["paths"]["executables"][key]
                print(key, "path set to:", self.paths["executables"][key])

            for key in config["available_options"]:
                self.available_options[key] = config["available_options"][key]

            self.paths["certificate"]["cert_file"] = config["paths"]["certificate"]["cert_file"]
            self.paths["certificate"]["key_file"] = config["paths"]["certificate"]["key_file"]
            self.port_number = int(os.getenv('LISTENING_PORT', '12345'))
            self.cors_origins = os.getenv('API_URL', 'localhost')

            self.max_chars_output = int(config["output"]["max_chars"])
            print("max_chars_output is:", self.max_chars_output)

            for key in config["limits"]:
                self.limits[key] = config["limits"][key]
                print(key, "limit set to:", self.limits[key])


config = Config()
