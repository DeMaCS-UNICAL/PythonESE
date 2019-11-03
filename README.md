# PythonESE
_PythonESE_ is a Python web app to execute logic programs with different solvers, using the [EmbASP](https://github.com/DeMaCS-UNICAL/EmbASP) framework.

## IMPORTANT NOTE
__*The project is still at an early stage of development*__  
__*It currently supports only 3 solvers (DLV, clingo, DLV2) and one formalism (Answer Set Programming).*__  
__*We encourage any feedback, but we do NOT recommend it for production yet.*__

## Getting Started (Installation and Usage)
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
It requires only [Python&reg;](https://www.python.org) and the [Tornado](https://www.tornadoweb.org) package.

### Installing
Download the [Latest Release](../../releases/latest) of _PythonESE_

Install via `pip` or

```
 python setup.py install
```

Note that on Linux systems you may need to change the _Execute_ permission of the files in the [executacles](https://github.com/DeMaCS-UNICAL/PythonESE/executacles) folder.

### Running
Can be invoked using the WebSocket protocol, as explained in the [Wiki of _EmbASPServerExecutor_](https://github.com/DeMaCS-UNICAL/EmbASPServerExecutor/wiki/APIs)

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
