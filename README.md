# GIMS Parsing

Parse GIMS :page_facing_up: PDF-based PGx reports to stuctured :star: star alleles.

The `parse.py` script reads all PDF files provided in the `data` directory and creates JSON files containing star allele information in the `results` directory.

## Docker Setup

* Clone this repo and start a terminal in the repository directory
* Build the Docker image `docker build -t gims-parsing .`
* Run the script using Docker `docker run -v $(pwd):/gims-parsing gims-parsing python3 parse.py`

## Manual Setup

Of course you can also setup everything without Docker and execute the `parse.py` script; please refer to the Dockerfile for required packages.
