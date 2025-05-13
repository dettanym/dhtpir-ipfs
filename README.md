# Peer2PIR : PIR Evaluation

This repository contains the code for evaluating PIR protocols in the literature.

## Requirements
* Docker
* Python 3

## Usage
Our code runs PIR protocols:

* [SealPIR](https://github.com/microsoft/SealPIR)
* [FastPIR](https://github.com/ishtiyaque/FastPIR)
* [OnionPIR](https://github.com/mhmughees/Onion-PIR)
* [Spiral (and variants)](https://github.com/menonsamir/spiral)
* [RLWEPIR (our work)](https://github.com/dettanym/private-zikade)

The evaluation is done in a Docker container. The code captures the results and processses them into a CSV file.
We capture two metrics, the server runtime and the total communication cost. The code captures the results and processes them into a CSV file.
The following command will run the evaluation and produce the results:

1. Select the desired number of rows and payload sizes in `run.py` (line 253 and 254)
2. Run ./run-exp to start the evaluation (which might take a while). The results will be logged in the `logs` directory.
3. Run the code in `plot.ipynb` to plot the results and generate the csv file of the results.
