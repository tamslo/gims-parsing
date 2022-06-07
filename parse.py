from getRawData import getRawData
from adaptRawData import adaptRawData
import json
import os

DATA_PATH = "data"
RESULTS_PATH = "results"
PDF_ENDING = ".pdf"
JSON_ENDING = ".json"

for fileName in os.listdir(DATA_PATH):
    if fileName.endswith(PDF_ENDING):
        filePath = os.path.join(DATA_PATH, fileName)
        rawData = getRawData(filePath)
        adaptedData = adaptRawData(rawData)
        # TODO: Check CPIC definition of ambiguous diplotypes
        # TODO: Prettier phenotype and check with CPIC API, e.g., https://api.cpicpgx.org/v1/diplotype?genesymbol=eq.CYP2B6&diplotype=eq.*1/*6
        jsonPath = filePath.replace(
            DATA_PATH, RESULTS_PATH, 1).replace(PDF_ENDING, JSON_ENDING)
        with open(jsonPath, 'w') as jsonFile:
            json.dump(adaptedData, jsonFile)
