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
- ``getDefaultDir`` required the pattern to be followed by a separator, which broke matching the
  documented ``BepiPred3_src`` folder name (no separator between the tool name and its version
  digit); now also accepts a digit immediately after the pattern.
- Exercised every selectable MHC-I/MHC-II method (not just the default), which surfaced six more
  real bugs, all fixed: a column-index mismatch affecting 5 of MHC-I's 8 methods and MHC-II's
  Consensus method (each real IEDB tool output format has a different column layout depending on
  the method); ``filterAlleles`` crashing instead of skipping an allele unsupported by the chosen
  method; MHC-II's predefined allele groups silently producing an empty allele list for 4 of its 6
  methods due to an "HLA-" prefix mismatch; "PickPocket-1.1" passing a mistyped, non-ASCII method
  name to the real tool; and MHC-II's "Consensus-2.2" using the wrong internal method/allele-file
  name. Added permanent test coverage for every method and for the previously entirely untested
  "label an existing set of sequence ROIs" input mode. NetMHC_Cons (MHC-I) reproducibly fails
  inside the vendored IEDB package itself in this environment; left alone as third-party code.
