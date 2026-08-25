# **************************************************************************
# *
# * Authors:     Daniel Del Hoyo (ddelhoyo@cnb.csic.es)
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

from pwem.protocols import EMProtocol
from pyworkflow.protocol import params

from pwchem.objects import Sequence, SequenceROI, SetOfSequenceROIs

from .. import Plugin as bepiPlugin
from ..constants import BEPIPRED_DIC
from ..protocols.protocol_mhc_ii_predict import ProtMHCIIPrediction

class ProtBepiPredPrediction(ProtMHCIIPrediction):
  """Run a prediction using BepiPred to extract B-cell epitopes"""
  _label = 'bepipred prediction'

  def __init__(self, **kwargs):
    EMProtocol.__init__(self, **kwargs)

  def _defineParams(self, form):
    form.addSection(label='Input')
    iGroup = self._defineInputParams(form)

    pGroup = form.addGroup('Parameters')
    pGroup.addParam('predType', params.EnumParam, label='Prediction type: ', default=0, choices=["mjv_pred", "vt_pred"],
                    help="Prediction model to use, either majority vote ensemble or variable threshold predicition "
                         "on average ensemble posistive probabilities")
    pGroup.addParam('top', params.FloatParam, label='Top proportion: ', default=0.2,
                    expertLevel=params.LEVEL_ADVANCED, help="Top proportion of epitope residues")
    pGroup.addParam('addSeqLen', params.BooleanParam, label='Add sequence length: ', default=False,
                    expertLevel=params.LEVEL_ADVANCED, help="Add sequence lengths to esm-encodings")

    pGroup.addParam('linearEp', params.BooleanParam, label='Extract linear epitopes: ', default=False,
                    help="Whether to pass a smoothing window over the results to extract linear epitopes")
    pGroup.addParam('rWindow', params.IntParam, label='Rolling window size: ', default=9, condition='linearEp',
                    help="Window size to use for rolling average on B-cell epitope probability scores.")

    eGroup = form.addGroup('Epitope extraction')
    eGroup.addParam('extractionMode', params.EnumParam, label='Extraction algorithm: ', default=0,
                    condition='inputSource==0',
                    choices=['Threshold + soft extension', 'Gap-tolerant sliding window'],
                    help="How to turn per-residue scores into epitope regions:\n"
                         "- Threshold + soft extension: scan residues in order, extending the current "
                         "epitope while the score passes the threshold (optionally tolerating a few "
                         "trailing near-threshold residues via the soft threshold below).\n"
                         "- Gap-tolerant sliding window: slide a fixed-size window over the scores; a "
                         "window passes if at most a few of its residues are below threshold, and every "
                         "residue covered by a passing window is marked positive. Passing residues are "
                         "then merged into contiguous regions. This tends to bridge short internal dips "
                         "without needing to tune a soft threshold by hand.")
    eGroup.addParam('avThres', params.FloatParam, label='Average threshold: ', default=0.1512,
                    condition='inputSource==0',
                    help="Threshold to use, when making predictions for considering a residue to be epitope positive")
    eGroup.addParam('useSoft', params.BooleanParam, label='Use a soft threshold: ', default=False,
                    expertLevel=params.LEVEL_ADVANCED, condition='inputSource==0 and extractionMode==0',
                    help="Use a soft threshold when extracting the epitopes by score")
    eGroup.addParam('softThres', params.FloatParam, label='Soft threshold: ', default=0.1,
                    expertLevel=params.LEVEL_ADVANCED, condition='inputSource==0 and extractionMode==0 and useSoft',
                    help="Soft threshold to use. If the score of a negative residue between two positive residues is "
                         "over the threshold-(threshold*softThreshold), it is also included as positive")
    eGroup.addParam('nSoft', params.IntParam, label='Soft threshold size: ', default=1,
                    expertLevel=params.LEVEL_ADVANCED, condition='inputSource==0 and extractionMode==0 and useSoft',
                    help="Defines N as the number of residues for which the soft threshold can be applied sequentially."
                         "If the score of N negative residue between two positive residues are "
                         "over threshold-(threshold*softThreshold), they are also included as positive")

    eGroup.addParam('windowSize', params.IntParam, label='Sliding window size: ', default=9,
                    condition='inputSource==0 and extractionMode==1',
                    help="Window size for the gap-tolerant sliding window algorithm (9 aa by default, the "
                         "minimum B-cell recognition footprint).")
    eGroup.addParam('maxGapResidues', params.IntParam, label='Max gap residues per window: ', default=2,
                    condition='inputSource==0 and extractionMode==1',
                    help="Individual below-threshold residues tolerated within a single window, so a real "
                         "epitope is not split or discarded because of a single weak residue.")

    eGroup.addParam('setSize', params.BooleanParam, label='Set epitope size limits: ', default=False,
                    condition='inputSource==0',
                    help="Whether to establish minimum and maximum epitope size")
    eGroup.addParam('minSize', params.IntParam, label='Minimum epitope size: ', default=3,
                    condition='inputSource==0 and setSize', help="Minimum epitope size")
    eGroup.addParam('maxSize', params.IntParam, label='Maximum epitope size: ', default=15,
                    condition='inputSource==0 and setSize', help="Maximum epitope size")


  def _insertAllSteps(self):
    self._insertFunctionStep(self.bepipredStep)
    self._insertFunctionStep(self.createOutputStep)

  def writeInputFasta(self):
    faFile = self._getExtraPath('inputSequence.fa')
    if self.inputSource.get() == 0:
      self.inputSequence.get().exportToFile(faFile)
    else:
      self.inputSequenceROIs.get().getSequenceObj().exportToFile(faFile)
    return os.path.abspath(faFile)

  def bepipredStep(self):
    faFile = self.writeInputFasta()
    oDir = os.path.abspath(self._getExtraPath())

    bepiArgs = f'-i {faFile} -o {oDir} -esm_dir {bepiPlugin.getVar(BEPIPRED_DIC["home"])} ' \
               f'-pred {self.getEnumText("predType")} -t {self.avThres.get()} -top {self.top.get()} '
    if self.linearEp.get():
      bepiArgs += f'-rolling_window_size {self.rWindow.get()} '
    if self.addSeqLen.get():
      bepiArgs += '-add_seq_len '

    bepiPlugin.runBepiPred(self, bepiArgs)

  def createOutputStep(self):

    outROIs = SetOfSequenceROIs(filename=self._getPath('sequenceROIs.sqlite'))
    if self.inputSource.get() == 0:
      if self.extractionMode.get() == 0:
        epiDic = self.parseResults(minLen=self.minSize.get(), maxLen=self.maxSize.get(), threshold=self.avThres.get(),
                                   softThres=self.softThres.get(), softN=self.nSoft.get())
      else:
        minLen = self.minSize.get() if self.setSize.get() else 1
        epiDic = self.parseResultsWindowVote(min_length=minLen, threshold=self.avThres.get(),
                                             window_size=self.windowSize.get(), max_gap_residues=self.maxGapResidues.get())

      inpSeq = self.inputSequence.get()
      for idxI, (epitope, score) in epiDic[list(epiDic.keys())[0]].items():
        idxs = [idxI, idxI+len(epitope)]
        roiSeq = Sequence(sequence=epitope, name='ROI_{}-{}'.format(*idxs), id='ROI_{}-{}'.format(*idxs),
                          description=f'BepiPred epitope')
        seqROI = SequenceROI(sequence=inpSeq, seqROI=roiSeq, roiIdx=idxs[0], roiIdx2=idxs[1])
        seqROI._epitopeType = params.String('B')
        seqROI._source = params.String('BepiPred')
        setattr(seqROI, 'BepiPred', params.Float(score))
        outROIs.append(seqROI)

    else:
      roiScores = self.parseResultsLabel()
      for roi in self.inputSequenceROIs.get():
        setattr(roi, 'BepiPred', params.Float(roiScores[roi.getObjId()]))
        outROIs.append(roi)


    if len(outROIs) > 0:
      self._defineOutputs(outputROIs=outROIs)

  ##################### UTILS #####################

  def parseResultsLabel(self):
    '''Parse the Bepipred output of score per residue and caluclates the average score for the resiudes of each of the
    input ROIs: {roiObjId: avScore}'''
    oDir = self._getExtraPath()
    scores = []
    with open(os.path.join(oDir, 'raw_output.csv')) as f:
      f.readline()
      for line in f:
        # rsplit, not split: BepiPred writes the sequence name+description verbatim as the
        # first field, and a comma in the description (e.g. "..., UniProt P0DTC9") would
        # otherwise be mistaken for a column separator.
        protId, res, score3D, scoreLinear = line.rsplit(',', 3)
        scores += [float(scoreLinear) if self.linearEp.get() else float(score3D)]

    roiScores = {}
    inROIs = self.inputSequenceROIs.get()
    for roi in inROIs:
      idx1, idx2 = roi.getROIIdxs()
      roiScores[roi.getObjId()] = sum(scores[idx1-1:idx2])/len(scores[idx1-1:idx2])
    return roiScores


  def parseResults(self, minLen, maxLen, threshold=0.1512, softThres=0.1, softN=1):
    '''Parse the results in the raw_output.csv file generated by BepiPred and returns a dictionary
    as {protId: {position: [epitope, meanScore]}} with the epitopes passing the threshold for BepiPred-3.0 linear epitope score.
    To pass the threshold, an epitope needs to have a lenght between minLen and maxLen.
    Also, all residue scores must be over the threshold or, optionally, between these residues there can be softN residues
    that passes the soft threshold, defined as thres-thres*softThres. This allows sort some close to the threshold
    residues inside the epitope.
    '''
    oDir = self._getExtraPath()

    epiDic = {}
    curEp, iniEp = '', -1
    with open(os.path.join(oDir, 'raw_output.csv')) as f:
      f.readline()
      for line in f:
        # rsplit: see parseResultsLabel() above, same comma-in-description issue.
        protId, res, score3D, scoreLinear = line.rsplit(',', 3)
        score = scoreLinear if self.linearEp.get() else score3D
        if protId not in epiDic:
          epiDic[protId] = {}
          i = 1
          curEp, iniEp, curSoft, scores = '', -1, 0, []

        if float(score) >= threshold:
          # If the threshold is passed
          if not curEp:
            # Save protein position
            iniEp = i
          # Add residue to epitope, initilize soft threshold
          curEp += res
          scores.append(float(score))
          curSoft = 0

        elif self.useSoft.get() and curEp and float(score) >= (threshold - threshold * softThres) and curSoft < softN:
          # If we have started defining an epitope and the soft thershold is passed, add residue to epitope
          curSoft += 1
          curEp += res
          scores.append(float(score))

        else:
          # If nor threshold is passed
          if curSoft > 0:
            # If last added position(s) was soft threshold, remove them
            curEp = curEp[:-curSoft]
          if len(scores) > 0:
            if not self.setSize.get() or (len(curEp) >= minLen and len(curEp) <= maxLen):
              # Save current epitope if the len conditions are met
              epiDic[protId][iniEp] = [curEp, sum(scores)/len(scores)]
            # Initialize current epitope
            curEp, iniEp, curSoft, scores = '', -1, 0, []

        i += 1

    if (not self.setSize.get() or (len(curEp) >= minLen and len(curEp) <= maxLen)) and len(scores) > 0:
      # Save current epitope if the len conditions are met
      epiDic[protId][iniEp] = [curEp, sum(scores) / len(scores)]
    return epiDic

  def parseResultsWindowVote(self, min_length, threshold=0.1512, window_size=9, max_gap_residues=2):
    '''Alternative to parseResults(): instead of a single left-to-right greedy scan with a trailing
    soft threshold, slide a fixed-size window over the per-residue scores. A window passes if at most
    max_gap_residues of its residues are below threshold, and every residue covered by a passing window
    is marked positive. Passing residues are then merged into contiguous regions of at least min_length
    residues. Returns the same {protId: {position: [epitope, meanScore]}} shape as parseResults(), so
    createOutputStep() does not need to know which mode produced it.
    '''
    oDir = self._getExtraPath()

    perProtein = {}
    with open(os.path.join(oDir, 'raw_output.csv')) as f:
      f.readline()
      for line in f:
        # rsplit: see parseResultsLabel() above, same comma-in-description issue.
        protId, res, score3D, scoreLinear = line.rsplit(',', 3)
        score = float(scoreLinear if self.linearEp.get() else score3D)
        perProtein.setdefault(protId, {'residues': [], 'scores': []})
        perProtein[protId]['residues'].append(res)
        perProtein[protId]['scores'].append(score)

    epiDic = {}
    for protId, data in perProtein.items():
      residues, scores = data['residues'], data['scores']
      n = len(residues)
      passing = [False] * n
      for i in range(n - window_size + 1):
        windowScores = scores[i:i + window_size]
        nBelow = sum(1 for s in windowScores if s < threshold)
        if nBelow <= max_gap_residues:
          for j in range(i, i + window_size):
            passing[j] = True

      epiDic[protId] = {}
      start = None
      for i in range(n + 1):
        if i < n and passing[i]:
          if start is None:
            start = i
        elif start is not None:
          length = i - start
          if length >= min_length:
            epitope = ''.join(residues[start:i])
            meanScore = sum(scores[start:i]) / length
            # 1-indexed protein position, matching parseResults()
            epiDic[protId][start + 1] = [epitope, meanScore]
          start = None

    return epiDic

  @classmethod
  def validateInstallation(cls):
    return bepiPlugin.validateBepiPredInstallation()

  def _validate(self):
    return []

  def _warnings(self):
    return []
