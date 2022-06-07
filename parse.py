import pdfplumber
import os

DATA_PATH = "data"
RESULTS_PATH = "results"
PDF_ENDING = ".pdf"
JSON_ENDING = ".json"
SPECIAL_WILDTYPE_ALLELE_NAMES = {}

def getGenotypeDetailTable(pdfPath):
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
    if 'wildtype' in diplotypeText:
        wildtypeAlleleName = '*1'
        if gene in SPECIAL_WILDTYPE_ALLELE_NAMES:
            wildtypeAlleleName = SPECIAL_WILDTYPE_ALLELE_NAMES[gene]
        diplotypeText = diplotypeText.replace('wildtype', wildtypeAlleleName)
    if ' or ' in diplotypeText:
        diplotype = diplotypeText.split(' or ')
        unambiguous = False
    else:
        diplotype = [diplotypeText]
        unambiguous = True        
    return diplotype, unambiguous

def getStarAllelesFromGenotypeTable(genotypeTable):
    starAlleles = {}
    for row in genotypeTable[1:]:
        gene = row[0]
        diplotypeText = row[1]
        diplotype, unambiguous = getDiplotype(gene, diplotypeText)
        starAlleles[gene] = {
            'diplotype': diplotype,
            'unambiguous': unambiguous
        }
    return starAlleles

for fileName in os.listdir(DATA_PATH):
    if fileName.endswith(PDF_ENDING):
        filePath = os.path.join(DATA_PATH, fileName)
        genotypeTable = getGenotypeDetailTable(filePath)
        starAlleles = getStarAllelesFromGenotypeTable(genotypeTable)
        # TODO: Check wildtype alleles (see constants above)
        # TODO: Write to JSON
        # TODO: Double check diplotypes (maybe with CPIC API, e.g., https://api.cpicpgx.org/v1/diplotype?genesymbol=eq.CYP2B6&diplotype=eq.*1/*6)
