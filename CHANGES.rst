=========
CHANGES
=========

3.0.0
=====
- Current feature set: BepiPred-3.0 linear B-cell epitope prediction, IEDB ``mhc_i``/``mhc_ii``
  MHC-I and MHC-II epitope prediction (8 selectable methods for MHC-I, including NetMHCpan),
  class-I immunogenicity prediction over pMHC complexes, MHC population coverage, and ElliPro
  conformational B-cell epitope prediction over atomic structures.
- ``validateInstallation`` only checked the BepiPred install; extended to also validate the MHC-I,
  MHC-II, population coverage, immunogenicity and ElliPro installs, so a missing/incomplete DTU
  tar for any of them is reported instead of only surfacing as a runtime failure.
