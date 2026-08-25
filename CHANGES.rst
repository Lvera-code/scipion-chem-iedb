=========
CHANGES
=========

3.0.0
=====
- Current feature set: BepiPred-3.0 linear B-cell epitope prediction (absorbed from the formerly
  separate ``scipion-chem-bepipred`` plugin, including its gap-tolerant sliding-window
  epitope-extraction mode as a second, selectable algorithm), IEDB ``mhc_i``/``mhc_ii`` MHC-I and
  MHC-II epitope prediction (8 and 6 selectable methods respectively, including NetMHCpan and
  NetMHCIIpan), class-I immunogenicity prediction over pMHC complexes, MHC population coverage, and
  ElliPro conformational B-cell epitope prediction over atomic structures.
- ``validateInstallation`` only ever checked the BepiPred install, silently passing even when
  another package was never configured; each protocol now validates only the single package it
  actually needs, and the plugin-wide check (used by the plugin manager) validates all six.
- BepiPred writes the imported sequence's name and description verbatim, unescaped, as the first
  column of ``raw_output.csv``; a comma anywhere in the description (a common thing to have, e.g.
  "..., UniProt P0DTC9") made every downstream parser (``parseResults``, ``parseResultsLabel``,
  ``parseResultsWindowVote``) crash on a naive ``line.split(',')``. Switched all three to
  ``line.rsplit(',', 3)``, which is immune to commas anywhere before the fixed 3 trailing columns.
- ``ProtMHCIIPrediction.mergeCoreData`` initialized its "best score so far" sentinel to 0 for the
  Score selection type, on the assumption that a real score would eventually exceed it; methods
  that report negative or zero raw scores for large parts of the peptide space (e.g. Sturniolo)
  could leave every core's best-epitope key at its initial ``(None, None)``, crashing
  ``createOutputStep`` with ``TypeError: object of type 'NoneType' has no len()``. The sentinel is
  now ``+/-inf`` depending on the actual comparison direction, and ``mergeAllelesEpitopes`` was
  cleaned up the same way for consistency.
- Both ``ProtMHCIPrediction`` and ``ProtMHCIIPrediction`` used the human-readable method label
  (e.g. ``MHCI_SMM-1.0``, dot included) as a dynamic output-object attribute name; pyworkflow's
  sqlite mapper reads a dot in a persisted attribute name as a nested-attribute separator, silently
  corrupting the object the next time it is loaded from disk (as happens whenever its ROIs are fed
  into a later protocol, e.g. Population Coverage) with ``KeyError`` on the truncated attribute
  name. Added ``sanitizeAttrName`` (replaces every non-alphanumeric character with ``_``) and use
  it for the attribute name specifically, while the human-readable label is kept everywhere it is
  only stored as a value.
- ``getDefaultDir`` resolved a package's home directory by a bare substring match against the
  ``EM_ROOT`` directory listing; since ``mhc_i`` is itself a substring of ``mhc_ii``, this could
  silently resolve MHC-I's home to the MHC-II install directory (or vice versa) depending on
  filesystem listing order. Now requires the pattern to match the whole directory name, or be
  followed by a separator or a digit (so folder names like ``BepiPred3_src`` still match).
- ``ProtBepiPredPrediction`` inherited ``ProtMHCIIPrediction``'s ``_validate()``, which reads a
  ``lengths`` parameter BepiPred's own form never defines, crashing before the protocol could run;
  restored an explicit no-op override.
- The vendored ``predict_immunogenicity.py`` script requires Python 2; ``defineBinaries`` now
  creates a dedicated ``immunogenicity-1.1`` conda env for it at install time (like BepiPred's own
  env), so users no longer have to build one themselves and wire it in through scipion.conf.
  ``runImmunogenicity`` activates that env (``IMMUNO_ACTIVATION_CMD``, overridable) instead of
  calling a configured interpreter path directly.
- ``predict_binding.py``'s real output has a different column layout per MHC-I method (netmhcpan:
  10 columns, includes core/icore; ann/smm/smmpmbec/comblib_sidney2008/pickpocket: 8 columns;
  consensus: 13 columns, one rank per submethod, no single ic50), which the code assumed was
  always netmhcpan's layout, crashing for 5 of the other 7 methods. Fixed with negative column
  indices (rank is always the last column, ic50/score always the second to last, regardless of the
  total column count) plus a dedicated column and a validation error for consensus, which has no
  single ic50 value. The same class of fix applies on the MHC-II side for its Consensus method
  (24 columns, its own rank column, no single score value).
- "PickPocket-1.1" passed the literal string ``pìckpocket`` (an accented i) to the real tool, which
  rejects it outright as an unknown method name.
- ``filterAlleles`` crashed with a ``KeyError`` whenever a predefined allele wasn't supported by the
  chosen MHC-I method (e.g. comblib_sidney2008 only covers 14 of them); now skips it instead.
- MHC-II's predefined allele groups (DR7, MHCII_FREQ) are written without the "HLA-" prefix, while
  four of its six methods' own allele files use it, silently producing an empty allele list and a
  failing tool invocation. Added ``matchAllelesToMethod()`` to normalize both sides before matching.
- MHC-II's "Consensus-2.2" method mapped to the internal key ``consensus``, but the real tool and
  allele-file name is ``consensus3``.
- Documented the MHC-I, MHC-II, population coverage, immunogenicity and ElliPro packages as
  directly downloadable (no license request form, unlike BepiPred's separate DTU service), and
  added the previously-missing download instructions for the immunogenicity and ElliPro packages.
- Added test coverage for every selectable MHC-I/MHC-II method and for the "label an existing set
  of sequence ROIs" input mode, neither of which had any coverage before. NetMHC_Cons (one of
  MHC-I's methods) reproducibly fails inside the vendored IEDB package itself, independent of any
  input; left unaddressed as third-party code.
