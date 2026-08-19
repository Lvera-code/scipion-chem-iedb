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
  MHC-II, population coverage, immunogenicity and ElliPro installs, so a missing/incomplete
  package is reported instead of only surfacing as a runtime failure. Each protocol now overrides
  ``validateInstallation`` with its own single-package check, so running one protocol no longer
  requires every package this plugin bundles to be installed.
- ``getDefaultDir`` resolved a package's home directory by a bare substring match against the
  ``EM_ROOT`` directory listing; since ``mhc_i`` is itself a substring of ``mhc_ii``, this could
  silently resolve MHC-I's home to the MHC-II install directory (or vice versa) depending on
  filesystem listing order. Now requires the pattern to match the whole directory name or be
  followed by a separator.
- ``ProtBepiPredPrediction`` inherited ``ProtMHCIIPrediction``'s ``_validate()``, which reads a
  ``lengths`` parameter BepiPred's own form never defines, crashing before the protocol could run;
  restored an explicit no-op override.
- Absorbed the BepiPred protocol previously maintained as a separate plugin
  (``scipion-chem-bepipred``, now deprecated), including its gap-tolerant sliding-window
  epitope-extraction mode as a second, selectable extraction algorithm.
- The vendored ``predict_immunogenicity.py`` script requires Python 2; ``runImmunogenicity`` now
  uses a configurable ``IMMUNO_PYTHON_BIN`` interpreter instead of a hardcoded ``python`` call.
- Documented the MHC-I, MHC-II, population coverage, immunogenicity and ElliPro packages as
  directly downloadable (no license request form, unlike BepiPred's separate DTU service), and
  added the previously-missing download instructions for the immunogenicity and ElliPro packages.
- Verified end to end (real downloads, real installs, real ``scipion3 test`` runs, not mocked):
  BepiPred (both extraction modes), MHC-I, MHC-II, population coverage, immunogenicity and ElliPro
  all pass.
