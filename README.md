# PythonESE
_PythonESE_ is a Python web app to execute logic programs with different solvers, using the [EmbASP](https://github.com/DeMaCS-UNICAL/EmbASP) framework.

## IMPORTANT NOTE
__*The project is still at an early stage of development*__  
__*It currently supports only the following formalisms and solvers:*__  

- ASP (Answer Set Programming)
  - DLV2
  - DLV
  - Clingo
- Datalog
  - I-DLV
  
__*We encourage any feedback, but we do NOT recommend it for production yet.*__

# Getting Started (Installation and Usage)
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
It requires only [Python&reg;](https://www.python.org) and the [Tornado](https://www.tornadoweb.org) package.

## Installing
Download the [Latest Release](../../releases/latest) of _PythonESE_

Install via `pip` or

```
 python setup.py install
```

<!-- Note that on Linux systems you may need to change the _Execute_ permission of the files in the [executables](https://github.com/DeMaCS-UNICAL/PythonESE/executables) folder. -->

## Running
Can be invoked using the WebSocket protocol, as explained in the [Wiki of _EmbASPServerExecutor_](https://github.com/DeMaCS-UNICAL/EmbASPServerExecutor/wiki/APIs)

# Dockerization

This repository provides also Docker containerization for PythonESE.
Docker enables the encapsulation of the PythonESE Module within a lightweight, portable container, ensuring smooth deployment across various environments.

## Getting Started

Deploying PythonESE using Docker is straightforward:

### Installation

Ensure Docker is installed on your system (refer to the [official Docker documentation](https://docs.docker.com/get-docker/) for installation instructions). Then, clone this repository using the following command:

```bash
git clone https://github.com/DeMaCS-UNICAL/PythonESE.git
```

### Building the Docker Image

A Docker image is a package that contains all the necessary to run application and it's used to create Docker containers. To create one navigate to the cloned repository directory and build the Docker image using the provided Dockerfile:

```bash
docker build -t python-ese .
```

### Running the Docker Container

Once the Docker image is built, you can run a Docker container using the following command:

```bash
docker run -d --network host --mount type=bind,source=[your/path/to/config],target=/app/config python-ese
```

The `--network host` option in the docker run command tells Docker to use the host network for the container. This means the container shares the same network stack as the host and can access network services running on the host directly.

The `--mount type=bind, source=[your/path/to/config], target=/app/config` option is used to create a bind mount. A bind mount is a type of mount that allows you to map a host file or directory to a container file or directory (for more information refer to the [official Docker documentation](https://docs.docker.com/storage/bind-mounts/)).
In this case we use mounts to provide the configuration file to the container. 

The configuration file is a JSON file that contains the configuration of PythonESE. It must be placed in a directory on the host and the _full_ path to this directory must be specified in the source option of the --mount option. The JSON schema needs also to be in the same directory.

For examples on how to create or modify the configuration file refer to the next section. If no configuration file is provided the default configuration will be used.

# Configuration

## config.json
This configuration file contains the settings for the PythonESE module. 

### Paths

This section contains paths to various resources.

- `executables`: Paths to different Logic Solvers like `dlv`, `clingo`, `dlv2`, `idlv`, and a timeout script(we use [this](https://github.com/pshved/timeout)).
- `certificate`: Paths to the certificate and key files for secure communication.

### Server Properties

This section contains properties related to the server.

- `port_number`: The port number on which the server is running.
- `cors_origins`: A list of origins that are allowed to access the server resources.

### Output

This section contains properties related to the output of the logic solvers.

- `max_chars`: The maximum number of characters that the output can contain.

### Limits

This section contains limits for the execution of the logic solvers.

- `time`: The maximum amount of time (in seconds) that the solver is allowed to run.
- `memory`: The maximum amount of memory (in kilobytes) that the solver is allowed to use.

### Available Options

This section contains options that can be passed to the logic solvers. Each solver has its own set of options.


## Built With
 - [EmbASP](https://www.mat.unical.it/calimeri/projects/embasp) - To execute logic programs with different solvers
 - [Tornado](https://www.tornadoweb.org) - To manage the web app
 - [timeout](http://coldattic.info/page/resourcelimit) - To limit time and memory consumption of the executors under Linux

<!-- 
## Contributing

Please read [CONTRIBUTING.md]() for details on our code of conduct, and the process for submitting pull requests to us.
 -->

## Versioning
We use [Semantic Versioning](http://semver.org) for versioning. For the versions available, see the [releases on this repository](https://github.com/DeMaCS-UNICAL/PythonESE/releases). 


## Credits
 - Stefano Germano

From the [Department of Mathematics and Computer Science](https://www.mat.unical.it) of the [University of Calabria](http://unical.it) and the [Department of Computer Science](http://www.cs.ox.ac.uk) of the [University of Oxford](http://www.ox.ac.uk)


## License
  This project is licensed under the [MIT License](LICENSE)
