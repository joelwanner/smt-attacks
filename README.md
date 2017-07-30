# SMTDoS

SMTDoS is a tool capable of finding possible Denial-of-Service attacks
in networks using an SMT-based approach.

## Getting Started

### Dependencies

SMTDoS requires Python 3.

The application relies on the [Z3](http://z3prover.github.io) theorem prover.
In order to install Z3, follow the [instructions](https://github.com/Z3Prover/z3#python)
in the Github repository for the Python bindings.

We use [BRITE](https://www.cs.bu.edu/brite) to generate random topologies.
BRITE is no longer supported, but a patched version can be obtained on
[Github](https://github.com/joelwanner/brite-patch).

Network attacks are visualized using [pydot](https://github.com/erocarrera/pydot),
which is a Python interface to the DOT graph description language.

### Usage

No further installation is required upon cloning the repository and installing the required dependencies.

For a list of commands, use

```
python src/smtdos.py --help
```

### Benchmarks

Generate network files for benchmarking and run them using the following commands:

```
python src/smtdos.py --generate crafted
python src/smtdos.py --generate random
python src/smtdos.py --benchmark examples
```

## Authors

* Joel Wanner – [Github](https://github.com/joelwanner)

Supervised by
* Prof. Dr. Adrian Perrig
* Samuel Hitz

## License

This project is licensed under the MIT License – see the [LICENSE.txt](LICENSE.txt) file for details.
Third-party licenses are included in the [LICENSES.txt](LICENSES.txt) file.
