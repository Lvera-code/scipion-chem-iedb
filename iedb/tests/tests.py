# **************************************************************************
# *
# * Authors:     Daniel Del Hoyo (ddelhoyo@cnb.csic.es)
# *
# * Unidad de Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307 USA
# *
# * All comments concerning this program package may be sent to the
# * e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

from pyworkflow.tests import setupTestProject, DataSet, BaseTest

from pwem.protocols import ProtImportSequence, ProtImportPdb

from pwchem.utils import assertHandle

from ..protocols import *


class BaseImportSeq(BaseTest):
	NAME = 'USER_SEQ'
	DESCRIPTION = 'User description'
	AMINOACIDSSEQ1 = 'MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHG'

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.ds = DataSet.getDataSet('model_building_tutorial')
		setupTestProject(cls)

		cls._runImportSeq()
		cls._waitOutput(cls.protImportSeq, 'outputSequences', sleepTime=5)

	@classmethod
	def _runImportSeq(cls):
		kwargs = {
			'inputSequenceName': cls.NAME,
			'inputSequenceDescription': cls.DESCRIPTION,
			'inputRawSequence': cls.AMINOACIDSSEQ1
		}

		cls.protImportSeq = cls.newProtocol(
			ProtImportSequence, **kwargs)
		cls.proj.launchProtocol(cls.protImportSeq, wait=False)


class TestBepiPredPrediction(BaseImportSeq):
	def _runBepiPredPrediction(self):
		protBepiPred = self.newProtocol(ProtBepiPredPrediction)

		protBepiPred.inputSequence.set(self.protImportSeq)
		protBepiPred.inputSequence.setExtended('outputSequence')

		self.proj.launchProtocol(protBepiPred, wait=False)
		return protBepiPred

	def test(self):
		protBepiPred = self._runBepiPredPrediction()
		self._waitOutput(protBepiPred, 'outputROIs', sleepTime=10)
		assertHandle(self.assertIsNotNone, getattr(protBepiPred, 'outputROIs', None))

class TestBepiPredPredictionWindowVote(TestBepiPredPrediction):
	'''Same as TestBepiPredPrediction but exercising the gap-tolerant sliding window extraction
	mode (extractionMode=1), the generic alternative to the default threshold + soft extension
	algorithm.'''

	def _runBepiPredPrediction(self):
		protBepiPred = self.newProtocol(ProtBepiPredPrediction, extractionMode=1)

		protBepiPred.inputSequence.set(self.protImportSeq)
		protBepiPred.inputSequence.setExtended('outputSequence')

		self.proj.launchProtocol(protBepiPred, wait=False)
		return protBepiPred

class TestMHCIPrediction(BaseImportSeq):
	def _runMHCIPrediction(self):
		protMHCI = self.newProtocol(ProtMHCIPrediction)

		protMHCI.inputSequence.set(self.protImportSeq)
		protMHCI.inputSequence.setExtended('outputSequence')

		self.proj.launchProtocol(protMHCI, wait=False)
		return protMHCI

	def test(self):
		protMHCI = self._runMHCIPrediction()
		self._waitOutput(protMHCI, 'outputROIs', sleepTime=10)
		assertHandle(self.assertIsNotNone, getattr(protMHCI, 'outputROIs', None))

class TestMHCIIPrediction(BaseImportSeq):
	def _runMHCIIPrediction(self):
		protMHCII = self.newProtocol(ProtMHCIIPrediction)

		protMHCII.inputSequence.set(self.protImportSeq)
		protMHCII.inputSequence.setExtended('outputSequence')

		self.proj.launchProtocol(protMHCII, wait=False)
		return protMHCII

	def test(self):
		protMHCII = self._runMHCIIPrediction()
		self._waitOutput(protMHCII, 'outputROIs', sleepTime=10)
		assertHandle(self.assertIsNotNone, getattr(protMHCII, 'outputROIs', None))

class TestMHCLabelROIs(BaseImportSeq):
	'''Exercises the "label an existing set of sequence ROIs" input mode (inputSource=1) of
	ProtMHCIPrediction/ProtMHCIIPrediction, instead of the default "predict over a full sequence"
	mode covered by TestMHCIPrediction/TestMHCIIPrediction.'''

	def _runBepiPredPrediction(self):
		protBepiPred = self.newProtocol(ProtBepiPredPrediction)

		protBepiPred.inputSequence.set(self.protImportSeq)
		protBepiPred.inputSequence.setExtended('outputSequence')

		self.proj.launchProtocol(protBepiPred, wait=False)
		return protBepiPred

	def _runBepiPredLabel(self, protROIs):
		protBepiPredLabel = self.newProtocol(ProtBepiPredPrediction, inputSource=1)

		protBepiPredLabel.inputSequenceROIs.set(protROIs)
		protBepiPredLabel.inputSequenceROIs.setExtended('outputROIs')

		self.proj.launchProtocol(protBepiPredLabel, wait=False)
		return protBepiPredLabel

	def _runMHCILabel(self, protROIs):
		protMHCI = self.newProtocol(ProtMHCIPrediction, inputSource=1)

		protMHCI.inputSequenceROIs.set(protROIs)
		protMHCI.inputSequenceROIs.setExtended('outputROIs')

		self.proj.launchProtocol(protMHCI, wait=False)
		return protMHCI

	def _runMHCIILabel(self, protROIs):
		protMHCII = self.newProtocol(ProtMHCIIPrediction, inputSource=1)

		protMHCII.inputSequenceROIs.set(protROIs)
		protMHCII.inputSequenceROIs.setExtended('outputROIs')

		self.proj.launchProtocol(protMHCII, wait=False)
		return protMHCII

	def test(self):
		protBepiPred = self._runBepiPredPrediction()
		self._waitOutput(protBepiPred, 'outputROIs', sleepTime=10)
		nInputROIs = len(protBepiPred.outputROIs)

		protMHCI = self._runMHCILabel(protBepiPred)
		self._waitOutput(protMHCI, 'outputROIs', sleepTime=10)
		assertHandle(self.assertIsNotNone, getattr(protMHCI, 'outputROIs', None))
		assertHandle(self.assertEqual, len(protMHCI.outputROIs), nInputROIs)
		assertHandle(self.assertTrue, all(hasattr(roi, '_allelesMHCI') for roi in protMHCI.outputROIs))

		protMHCII = self._runMHCIILabel(protBepiPred)
		self._waitOutput(protMHCII, 'outputROIs', sleepTime=10)
		assertHandle(self.assertIsNotNone, getattr(protMHCII, 'outputROIs', None))
		assertHandle(self.assertEqual, len(protMHCII.outputROIs), nInputROIs)
		assertHandle(self.assertTrue, all(hasattr(roi, '_allelesMHCII') for roi in protMHCII.outputROIs))

		protBepiPredLabel = self._runBepiPredLabel(protMHCI)
		self._waitOutput(protBepiPredLabel, 'outputROIs', sleepTime=10)
		assertHandle(self.assertIsNotNone, getattr(protBepiPredLabel, 'outputROIs', None))
		assertHandle(self.assertEqual, len(protBepiPredLabel.outputROIs), len(protMHCI.outputROIs))
		assertHandle(self.assertTrue, all(hasattr(roi, 'BepiPred') for roi in protBepiPredLabel.outputROIs))

class TestImmunogenicityPrediction(TestMHCIPrediction):
	def _runImmunogenicityPrediction(self, protROIs):
		protImmuno = self.newProtocol(ProtImmunogenicityPrediction)

		protImmuno.inputROIs.set(protROIs)
		protImmuno.inputROIs.setExtended('outputROIs')

		self.proj.launchProtocol(protImmuno, wait=False)
		return protImmuno

	def test(self):
		protMHC = self._runMHCIPrediction()
		self._waitOutput(protMHC, 'outputROIs', sleepTime=10)

		protImmuno = self._runImmunogenicityPrediction(protMHC)
		self._waitOutput(protImmuno, 'outputROIs', sleepTime=10)
		assertHandle(self.assertIsNotNone, getattr(protImmuno, 'outputROIs', None))

class TestMHCPopulationCoverage(TestMHCIIPrediction):
	def _runMHCCoverage(self, protMHC):
		protPop = self.newProtocol(
			ProtMHCPopulationCoverage,
			mhc=1,
			inAreas='Area'
		)

		protPop.inputSequenceROIs.set(protMHC)
		protPop.inputSequenceROIs.setExtended('outputROIs')

		self.proj.launchProtocol(protPop, wait=False)
		return protPop

	def test(self):
		protMHCII = self._runMHCIIPrediction()
		self._waitOutput(protMHCII, 'outputROIs', sleepTime=10)
		protPop = self._runMHCCoverage(protMHCII)
		self._waitOutput(protPop, 'outputROIs', sleepTime=10)
		assertHandle(self.assertIsNotNone, getattr(protPop, 'outputROIs', None))

class TestElliProPrediction(BaseTest):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.ds = DataSet.getDataSet('model_building_tutorial')
		setupTestProject(cls)

		cls._runImportPDB()
		cls._waitOutput(cls.protImportPDB, 'outputPdb', sleepTime=5)

	@classmethod
	def _runImportPDB(cls):
		cls.protImportPDB = cls.newProtocol(
			ProtImportPdb,
			inputPdbData=1,
			pdbFile=cls.ds.getFile('PDBx_mmCIF/5ni1.pdb')
		)
		cls.proj.launchProtocol(cls.protImportPDB, wait=False)

	def _runElliProPrediction(self):
		protElliPro = self.newProtocol(
			ProtElliProPrediction,
			rchains=True,
			chain_name='{"model": 0, "chain": "A", "residues": 92}'
		)

		protElliPro.inputAtomStruct.set(self.protImportPDB)
		protElliPro.inputAtomStruct.setExtended('outputPdb')

		self.proj.launchProtocol(protElliPro, wait=False)
		return protElliPro

	def test(self):
		protElliPro = self._runElliProPrediction()
		self._waitOutput(protElliPro, 'outputROIs', sleepTime=10)
		assertHandle(self.assertIsNotNone, getattr(protElliPro, 'outputStructROIs', None))
		assertHandle(self.assertIsNotNone, getattr(protElliPro, 'outSequenceROIs_A', None))
