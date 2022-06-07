import re

def _adaptDiplotype(diplotypeText, phenotypeText):
    if 'wildtype' in diplotypeText:
        diplotypeText = diplotypeText.replace('wildtype', '*1')
    if ', xN' in diplotypeText:
        diplotypeText = diplotypeText.replace(', xN', 'xN')
    if diplotypeText == 'X':
        diplotypeText = re.search('\*\d+\/\*\d+', phenotypeText).group(0)
    if ' or ' in diplotypeText:
        diplotypeText = diplotypeText.split(' or ')
    else:
        diplotypeText = [diplotypeText]
    return diplotypeText


def _adaptPhenotype(gene, phenotypeText):
    phenotypeText = phenotypeText.replace('\n', ' ').replace('  ', ' ')
    if 'METABOLIZER' in phenotypeText:
        phenotypeText = phenotypeText.replace(gene, '').strip()
    return phenotypeText

def adaptRawData(rawData):
    adaptedData = {}
    for gene in rawData:
        diplotype = _adaptDiplotype(rawData[gene]['diplotype'], rawData[gene]['phenotype'])
        phenotype = _adaptPhenotype(gene, rawData[gene]['phenotype'])
        adaptedData[gene] = {
            'diplotype': diplotype,
            'phenotype': phenotype
        }
    return adaptedData
