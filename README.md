# SMTDoS

SMTDoS is a tool to find possible Denial-of-Service attacks in networks using the Z3 theorem prover.
This is the code repository for the thesis *An SMT-Based Approach to Synthesizing Unknown Network Attacks*.

## Getting Started

### Dependencies

SMTDoS requires Python 3.

The application relies on the [Z3](http://z3prover.github.io) theorem prover.
In order to install Z3, follow the [instructions](https://github.com/Z3Prover/z3#python) in the Github repository for the python bindings.

[NetworkX](http://networkx.github.io) is used to generate networks, which are visualized using [pydot](https://github.com/erocarrera/pydot).

### Usage

Clone the repository to install SMTAX.

For a list of commands, use

```
python src/smtdos.py --help
```

### Benchmarks

Generate network files for benchmarking and run them using the following commands:

```
python src/smtdos.py --generate
python src/smtdos.py --benchmark
```

## Authors

* Joel Wanne – [Github](https://github.com/joelwanner)

Supervised by
* Prof. Dr. Adrian Perrig
* Samuel Hitz

## License

This project is licensed under the MIT License – see the [LICENSE.txt](LICENSE.txt) file for details
