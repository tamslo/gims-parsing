import pdfplumber
import json
import os

DATA_PATH = "data"
RESULTS_PATH = "results"
PDF_ENDING = ".pdf"
JSON_ENDING = ".json"
SPECIAL_WILDTYPE_ALLELE_NAMES = {}

def getGenotypeTable(pdfPath):
    genotypeTable = None
    with pdfplumber.open(pdfPath) as pdf:
        for page in pdf.pages:
            pageTables = page.extract_tables()
            for table in pageTables:
                tableHeader = table[0]
                if 'Genotyp' in tableHeader:
                    genotypeTable = table
                    break
            if genotypeTable is not None:
                break
    return genotypeTable

def getDiplotype(gene, diplotypeText):
    diplotype = None
    # if 'wildtype' in diplotypeText:
    #     wildtypeAlleleName = '*1'
    #     if gene in SPECIAL_WILDTYPE_ALLELE_NAMES:
    #         wildtypeAlleleName = SPECIAL_WILDTYPE_ALLELE_NAMES[gene]
    #     diplotypeText = diplotypeText.replace('wildtype', wildtypeAlleleName)
    if ' or ' in diplotypeText:
        diplotype = diplotypeText.split(' or ')
    else:
        diplotype = [diplotypeText]
    return diplotype

def getPhenotype(gene, phenotypeText):
    phenotypeText = phenotypeText.replace('\n', ' ').replace('  ', ' ')
    if 'METABOLIZER' in phenotypeText:
        phenotypeText = phenotypeText.replace(gene, '').strip()
    return phenotypeText

def getStarAlleleData(genotypeTable):
    starAlleles = {}
    for row in genotypeTable[1:]:
        gene = row[0]
        diplotypeText = row[1]
        diplotype = getDiplotype(gene, diplotypeText)
        phenotypeText = row[2]
        phenotype = getPhenotype(gene, phenotypeText)
        starAlleles[gene] = {
            'diplotype': diplotype,
            'phenotype': phenotype
        }
    return starAlleles

for fileName in os.listdir(DATA_PATH):
    if fileName.endswith(PDF_ENDING):
        filePath = os.path.join(DATA_PATH, fileName)
        genotypeTable = getGenotypeTable(filePath)
        starAlleleData = getStarAlleleData(genotypeTable)
        jsonPath = filePath.replace(
            DATA_PATH, RESULTS_PATH, 1).replace(PDF_ENDING, JSON_ENDING)
        with open(jsonPath, 'w') as jsonFile:
            json.dump(starAlleleData, jsonFile)
        # TODO: Check wildtype alleles (see above)
        # TODO: Check CPIC definition of ambiguous diplotypes
        # TODO: Prettier phenotype and check with CPIC API, e.g., https://api.cpicpgx.org/v1/diplotype?genesymbol=eq.CYP2B6&diplotype=eq.*1/*6
