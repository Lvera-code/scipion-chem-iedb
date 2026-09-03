from pyworkflow.tests import setupTestProject, DataSet, BaseTest
from pwem.protocols import ProtImportSequence
from pwchem.utils import assertHandle
from iedb.protocols import ProtMHCIPrediction, ProtMHCIIPrediction, ProtBepiPredPrediction

class TestAlternativeMethods(BaseTest):
    '''Exercises every selectable MHC-I/MHC-II method and BepiPred prediction mode other than the
    default one already covered by TestMHCIPrediction/TestMHCIIPrediction/TestBepiPredPrediction.
    NetMHC_Cons (MHC-I method index 2) is intentionally not covered here: it reproducibly fails
    inside the vendored IEDB mhc_i package itself in this environment, unrelated to this plugin's
    own code.'''

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ds = DataSet.getDataSet('model_building_tutorial')
        setupTestProject(cls)
        cls.protImportSeq = cls.newProtocol(
            ProtImportSequence,
            inputSequenceName='USER_SEQ',
            inputSequenceDescription='User description',
            inputRawSequence='MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHG')
        cls.proj.launchProtocol(cls.protImportSeq, wait=True)

    def _runMHCI(self, method, **kwargs):
        prot = self.newProtocol(ProtMHCIPrediction, method=method, **kwargs)
        prot.inputSequence.set(self.protImportSeq)
        prot.inputSequence.setExtended('outputSequence')
        self.proj.launchProtocol(prot, wait=True)
        return prot

    def _runMHCII(self, method, **kwargs):
        prot = self.newProtocol(ProtMHCIIPrediction, method=method, **kwargs)
        prot.inputSequence.set(self.protImportSeq)
        prot.inputSequence.setExtended('outputSequence')
        self.proj.launchProtocol(prot, wait=True)
        return prot

    def test_bepipred_vt(self):
        prot = self.newProtocol(ProtBepiPredPrediction, predType=1)  # vt_pred
        prot.inputSequence.set(self.protImportSeq)
        prot.inputSequence.setExtended('outputSequence')
        self.proj.launchProtocol(prot, wait=True)
        assertHandle(self.assertIsNotNone, getattr(prot, 'outputROIs', None))

    # MHC-I methods: 0 IEDB recommended, 1 Consensus-2.18, 2 NetMHC_Cons, 3 ANN-4.0,
    # 4 SMMPMBEC-1.0, 5 SMM-1.0, 6 Combinatorial Library-1.0, 7 PickPocket-1.1
    def test_mhci_consensus(self):
        prot = self._runMHCI(1)
        assertHandle(self.assertIsNotNone, getattr(prot, 'outputROIs', None))

    def test_mhci_ann(self):
        prot = self._runMHCI(3)
        assertHandle(self.assertIsNotNone, getattr(prot, 'outputROIs', None))

    def test_mhci_smmpmbec(self):
        prot = self._runMHCI(4)
        assertHandle(self.assertIsNotNone, getattr(prot, 'outputROIs', None))

    def test_mhci_smm(self):
        prot = self._runMHCI(5)
        assertHandle(self.assertIsNotNone, getattr(prot, 'outputROIs', None))

    def test_mhci_comblib(self):
        prot = self._runMHCI(6)
        assertHandle(self.assertIsNotNone, getattr(prot, 'outputROIs', None))

    def test_mhci_pickpocket(self):
        prot = self._runMHCI(7)
        assertHandle(self.assertIsNotNone, getattr(prot, 'outputROIs', None))

    # MHC-II methods: 0 IEDB recommended, 1 Consensus-2.2, 2 NN_align-1.0, 3 SMM_align-1.1,
    # 4 Combinatorial Library-1.1, 5 Sturniolo
    def test_mhcii_consensus(self):
        prot = self._runMHCII(1)
        assertHandle(self.assertIsNotNone, getattr(prot, 'outputROIs', None))

    def test_mhcii_nn_align(self):
        prot = self._runMHCII(2)
        assertHandle(self.assertIsNotNone, getattr(prot, 'outputROIs', None))

    def test_mhcii_smm_align(self):
        prot = self._runMHCII(3)
        assertHandle(self.assertIsNotNone, getattr(prot, 'outputROIs', None))

    def test_mhcii_comblib(self):
        prot = self._runMHCII(4)
        assertHandle(self.assertIsNotNone, getattr(prot, 'outputROIs', None))

    def test_mhcii_sturniolo(self):
        prot = self._runMHCII(5)
        assertHandle(self.assertIsNotNone, getattr(prot, 'outputROIs', None))
