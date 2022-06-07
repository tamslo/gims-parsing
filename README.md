# gims-parsing

Parse GIMS PDF-based PGx reports :page_facing_up: to stuctured :star: alleles.

The `gimsParsing.py` script reads all PDF files provided in the `data` directory and creates JSON files containing star allele information in the `results` directory.

## Docker Setup

* If not done yet, build the Docker image `docker build -t gims-parsing .`
* Run the script using Docker `docker run -v $(pwd):/gims-parsing gims-parsing python3 parse.py`

## Manual Setup

Of course you can also setup everything without Docker and execute the `gimsParsing.py` script; please refer to the Dockerfile for required packages.
