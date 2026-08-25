# **************************************************************************
# *
# * Authors:     Carlos Oscar Sorzano (coss@cnb.csic.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os
import re

from iedb import Plugin
from iedb.constants import POP_DIC

def sanitizeAttrName(name):
  '''pyworkflow's sqlite mapper reads a dot in a persisted object's attribute name as a nested
  attribute separator; a dynamic attribute name built from a method label containing a version
  number (e.g. "MHCI_SMM-1.0") silently corrupts the object on the next reload from disk. Replace
  any character that is not alphanumeric or an underscore before using a label as an attribute
  name (the human-readable label itself is kept intact wherever it is only stored as a value).'''
  return re.sub(r'\W', '_', name)

def getAllelesFile(mhc, method):
  return Plugin.getPluginHome(f'constants/alleles-{mhc}/{method.lower()}_alleles.txt')

def getAllMHCIAlleles(method, specie='human'):
  '''Parse the possible alleles given a method from the files stored in constants.
  Returns a dictionary of the form: {specie: {mhc: [lengths]}}'''
  alDic = {}
  alleFile = getAllelesFile('I', method)
  specie = specie.lower()
  with open(alleFile) as f:
    f.readlines(2)
    for line in f:
      sp, allele, l = line.split()
      if specie == sp:
        if allele not in alDic:
          alDic[allele] = []

        alDic[allele].append(l)
  return alDic

def getAllMHCIIAlleles(method, specie='human'):
  alleles = []
  if specie == 'human':
    alleFile = getAllelesFile('II', method)
    with open(alleFile) as f:
      f.readline()
      for line in f:
        alleles.append(line.strip())
  else:
    from ..constants import MOUSE_MHCII_ALLELES
    alleles = MOUSE_MHCII_ALLELES
  return alleles

def normalizeAlleleName(allele):
  '''Some MHC-II methods' allele lists carry an "HLA-" prefix and others do not (e.g. netmhciipan's
  "DRB1*03:01" vs nn_align's "HLA-DRB1*03:01" for the very same allele), while the predefined allele
  groups (DR7, MHCII_FREQ) are always written without it. Strip it for comparison purposes only.'''
  return allele[4:] if allele.startswith('HLA-') else allele

def matchAllelesToMethod(selAlleles, allowedAlleles):
  '''Maps a list of selected alleles (as written in a predefined allele group) to the equivalent
  entries in allowedAlleles (as written in a specific method's own allele file), regardless of
  whether either side carries the "HLA-" prefix.'''
  normAllowed = {normalizeAlleleName(a): a for a in allowedAlleles}
  return [normAllowed[normalizeAlleleName(allele)] for allele in selAlleles
          if normalizeAlleleName(allele) in normAllowed]

def getMHCAlleles(roi, mhc):
  alleles = []
  if hasattr(roi, '_allelesMHCI') and mhc in ['I', 'combined']:
    alleles += [getattr(roi, '_allelesMHCI').get().replace('/', ',')]

  if hasattr(roi, '_allelesMHCII') and mhc in ['II', 'combined']:
    alleles += [getattr(roi, '_allelesMHCII').get().replace('/', ',')]
  return ','.join(alleles)

def writeInputEpitopeFiles(inputROIs, epFile, separated, mhc):
  outFiles = []
  if separated:
    for roi in inputROIs:
      groupFile = epFile.replace('.tsv', f'_{roi.clone().getObjId()}.tsv')
      alleles = getMHCAlleles(roi, mhc)
      if alleles:
        with open(groupFile, 'w') as f:
          f.write(f'{roi.getROISequence()}\t{alleles}\n')
        outFiles.append(groupFile)
  else:
    epFile = epFile.replace('.tsv', f'_All.tsv')
    with open(epFile, 'w') as f:
      for roi in inputROIs:
        alleles = getMHCAlleles(roi, mhc)
        if alleles:
          f.write(f'{roi.getROISequence()}\t{alleles}\n')
    outFiles.append(epFile)

  return outFiles

def translateArea(pops):
  if 'Area' in pops:
    pops.remove('Area')
    pops += list(POP_DIC['Area'].keys())

  pops.sort()
  return pops

def buildMHCCoverageArgs(inputROIs, epFile, populations, mhc, oDir, separated=True):
  inEpiFiles = writeInputEpitopeFiles(inputROIs, epFile, separated, mhc)
  fullPopStr = '","'.join(populations)
  oDir = os.path.abspath(oDir)

  coveArgs = []
  for epFile in inEpiFiles:
    epFile = os.path.abspath(epFile)
    epBase = os.path.basename(epFile)
    oFile = os.path.join(oDir, epBase.replace('.tsv', '_results.tsv'))
    coveArgs += [f'-p "{fullPopStr}" -c {mhc} -f {epFile} > {oFile} ']
  return coveArgs

def parseCoverageResults(oFile, norm=True):
  oDic = {}
  with open(oFile) as f:
    if 'No result found!' not in f.readline():
      f.readline()
      for line in f:
        if line.strip():
          sline = line.split('\t')
          normVal = 100 if norm else 1
          oDic[sline[0]] = {'coverage': float(sline[1][:-2])/normVal, 'average_hit': sline[2], 'pc90': sline[3].strip()}
        else:
          break
    else:
      oDic['average'] = {'coverage': 0, 'average_hit': 0, 'pc90': 0}
  return oDic