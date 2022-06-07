import pdfplumber

def _getGenotypeTable(pdfPath):
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

def getRawData(pdfPath):
    genotypeTable = _getGenotypeTable(pdfPath)
    rawData = {}
    for row in genotypeTable[1:]:
        gene = row[0]
        diplotypeText = row[1]
        phenotypeText = row[2]
        rawData[gene] = {
            'diplotype': diplotypeText,
            'phenotype': phenotypeText
        }
    return rawData

    
