================================
IEDB scipion plugin
================================

Scipion framework plugin for the use of tools provided by IEDB epitope tools.
This plugin allows to use programs from the IEDB website for B-cell (BepiPred), MHC-I, MHC-II and
conformational (ElliPro) epitope predictions, class-I immunogenicity and population coverage within
the Scipion framework. **You need to download the IEDB files before installing the plugin, see
section "Download IEDB files" for details**.

================================
Download IEDB files
================================

IEDB contains several software packages for epitope prediction and other tools, distributed under
their own academic-use license terms. BepiPred is a separate DTU Health Tech service and must be
requested through the form linked below; the MHC-I, MHC-II, population coverage, immunogenicity and
ElliPro packages are directly downloadable, without any request form, from
https://downloads.iedb.org/tools/. Now, specific instructions for each of the packages will be
provided.

|

1. **B-cell epitope prediction**

Antibody Epitope Prediction tool contains collection of python scripts, specific binary for BepiPred and a pickled
file containing residue scales for different methods. The zip file can be downloaded from
https://services.healthtech.dtu.dk/cgi-bin/sw_request?software=bepipred&version=3.0&packageversion=3.0b&platform=src

Once you obtain the software file (a zip) you have several options to help Scipion finding it:

Option 1) Edit the scipion.conf file and add the variable: BEPIPRED_ZIP = <PathToBepiPredZip>.
This way, Scipion will unzip and move the corresponding files to the scipion/software/em folder and install BepiPred.

Option 2) If you have unzipped BepiPred yourself you can either:

2.1) Move the folder (of the form BepiPred3_src) to the scipion/software/em folder. Scipion will find it there.

2.2) Specify the location of the BepiPred folder in the scipion.conf file as: BEPIPRED_HOME = <PathToBepiPred3_src>

Option 3) If you have already installed BepiPred (creating the python environment needed), you need to specify Scipion in the scipion.conf file both:

3.a) The path to the BepiPred folder as: BEPIPRED_HOME = <PathToBepiPred3_src> and

3.b) The activation command as: BEPIPRED_ACTIVATION_CMD = <ActivationCommand>

This way, Scipion will use your own BepiPred installation.

|

2. **MHC-I epitope prediction**

The MHC_I binding tool contains a collection of following peptide binding prediction methods for Major
Histocompatibility Complex (MHC) class I molecules.The collection is a mixture of pythons scripts and linux
32-bit environment specific binaries. The tar file can be downloaded from
http://tools.iedb.org/mhci/download/

Once you obtain the software file (a tar.gz) you have several options to help Scipion finding it:

Option 1) Edit the scipion.conf file and add the variables:
 - MHC-I_TAR = <PathToMhc-ITar> (IEDB_MHC_I-3.1.5.tar.gz)

This way, Scipion will untar and move the corresponding files to the scipion/software/em folder and install mhc-i.

Option 2) If you have unzipped the mhc-i tars yourself you can either:

2.1) Move the folder (of the form mhc_i) to the scipion/software/em folder. Scipion will find it there.

2.2) Specify the location of the MHC folder in the scipion.conf file as: MHC-I_HOME = <PathToMhc-I_folder>

|

3. **MHC-II epitope prediction**

The MHC_II binding tool contains a collection of following peptide binding prediction methods for Major
Histocompatibility Complex (MHC) class II molecules.The collection is a mixture of pythons scripts and linux
32-bit environment specific binaries. The tar file can be downloaded from
http://tools.iedb.org/mhcii/download/

Once you obtain the software file (a tar.gz) you have several options to help Scipion finding it:

Option 1) Edit the scipion.conf file and add the variables:
 - MHC-II_TAR = <PathToMhc-IITar> (IEDB_MHC_II-3.1.5.tar.gz)

This way, Scipion will untar and move the corresponding files to the scipion/software/em folder and install mhc-ii.

Option 2) If you have unzipped the mhc-ii tars yourself you can either:

2.1) Move the folder (of the form mhc_ii) to the scipion/software/em folder. Scipion will find it there.

2.2) Specify the location of the MHC folder in the scipion.conf file as: MHC-II_HOME = <PathToMhc-II_folder>

|

4. **Population coverage tool**

Population Coverage tool contains collection of python scripts, a 'deps' directory as required/dependency,
which includes a pickled file containing all population coverage data (various population, alleles and frequencies)
and necessary python scripts. The tar file can be downloaded from
http://tools.iedb.org/population/download/

Once you obtain the software file (a tar.gz) you have several options to help Scipion finding it:

Option 1) Edit the scipion.conf file and add the variables:
 - COVERAGE_TAR = <PathToPopCoverageTar> (IEDB_Population_Coverage-3.0.2.tar.gz)

This way, Scipion will untar and move the corresponding files to the scipion/software/em folder and install mhc-ii.

Option 2) If you have unzipped the population_coverage tars yourself you can either:

2.1) Move the folder (of the form population_coverage) to the scipion/software/em folder. Scipion will find it there.

2.2) Specify the location of the MHC folder in the scipion.conf file as: COVERAGE_HOME = <PathToPopCoverage_folder>

|

5. **Class-I immunogenicity tool**

The immunogenicity tool contains a collection of python scripts to predict the immunogenicity of a
peptide-MHC (pMHC) complex. The tar file can be downloaded from
https://downloads.iedb.org/tools/immunogenicity/.

Once you obtain the software file (a tar.gz) you have several options to help Scipion finding it:

Option 1) Edit the scipion.conf file and add the variable:
 - IMMUNO_TAR = <PathToImmunogenicityTar> (IEDB_Immunogenicity-1.1.tar.gz)

This way, Scipion will untar and move the corresponding files to the scipion/software/em folder and
install immunogenicity.

Option 2) If you have unzipped the immunogenicity tar yourself you can either:

2.1) Move the folder (of the form immunogenicity) to the scipion/software/em folder. Scipion will
find it there.

2.2) Specify the location of the immunogenicity folder in the scipion.conf file as:
IMMUNO_HOME = <PathToImmunogenicity_folder>

The vendored ``predict_immunogenicity.py`` script is written for Python 2. If your system's own
``python`` no longer resolves to a Python 2 interpreter, point Scipion at one explicitly by setting
IMMUNO_PYTHON_BIN = <PathToPython2Binary> in the scipion.conf file (e.g. a dedicated
``conda create -n <env> python=2.7`` environment's interpreter).

|

6. **ElliPro tool**

ElliPro is distributed as a single Java jar file and predicts conformational (structural) B-cell
epitopes from an atomic structure. It can be downloaded from
https://downloads.iedb.org/tools/ellipro/, and requires a Java runtime to be available.

Once you obtain the jar file, point Scipion at it by editing the scipion.conf file and adding the
variable:
 - ELLIPRO_JAR = <PathToElliProJar> (ElliPro.jar)

Scipion will move the jar file into the scipion/software/em folder on install.


===================
Install this plugin
===================

You will need to use `3.0.0 <https://github.com/I2PC/scipion/releases/tag/v3.0>`_ version of Scipion
to run these protocols. To install the plugin, you have two options:

- **Stable version**

.. code-block::

      scipion installp -p scipion-chem-iedb

OR

  - through the plugin manager GUI by launching Scipion and following **Configuration** >> **Plugins**

- **Developer's version**

1. **Download repository**:

.. code-block::

            git clone https://github.com/scipion-chem/scipion-chem-iedb.git

2. **Switch to the desired branch** (main or devel):

Scipion-chem-iedb is constantly under development.
If you want a relatively older an more stable version, use main branch (default).
If you want the latest changes and developments, user devel branch.

.. code-block::

            cd scipion-chem-iedb
            git checkout devel

3. **Install**:

.. code-block::

            scipion installp -p path_to_scipion-chem-iedb --devel

- **Tests**

To check the installation, run the Scipion tests. BepiPred is the only tool this plugin's own test
suite is willing to run automatically, since it is the only one that does not require a DTU-licensed
tar download to already be configured in ``scipion.conf`` (see "Download IEDB files" above):

.. code-block::

            scipion3 tests iedb.tests.tests.TestBepiPredPrediction

The remaining tests exercise the MHC-I, MHC-II, population coverage, ElliPro and immunogenicity
protocols, and additionally require ``MHC_I_HOME``/``MHC_I_TAR``, ``MHC_II_HOME``/``MHC_II_TAR``,
``COVERAGE_HOME``/``COVERAGE_TAR`` and ``ELLIPRO_HOME``/``ELLIPRO_JAR`` to be set as described above:

.. code-block::

            scipion3 tests iedb.tests.tests.TestMHCIPrediction
            scipion3 tests iedb.tests.tests.TestMHCIIPrediction
            scipion3 tests iedb.tests.tests.TestImmunogenicityPrediction
            scipion3 tests iedb.tests.tests.TestMHCPopulationCoverage
            scipion3 tests iedb.tests.tests.TestElliProPrediction

===================
Protocols provided
===================

- **BepiPred prediction** (``ProtBepiPredPrediction``): linear B-cell epitope prediction over an
  input sequence using BepiPred-3.0, exposed as sequence ROIs.
- **MHC-I prediction** (``ProtMHCIPrediction``): MHC-I epitope prediction over an input sequence
  (or allele labelling of an existing set of sequence ROIs), using any of the methods bundled in
  IEDB's ``mhc_i`` package (IEDB-recommended/NetMHCpan, Consensus, NetMHCcons, ANN, SMM, SMMPMBEC,
  Combinatorial Library, PickPocket).
- **MHC-II prediction** (``ProtMHCIIPrediction``): MHC-II epitope prediction over an input sequence,
  using IEDB's ``mhc_ii`` package.
- **Immunogenicity prediction** (``ProtImmunogenicityPrediction``): scores the immunogenicity of the
  peptide-MHC (pMHC) complexes produced by the MHC-I protocol over a set of sequence ROIs.
- **MHC population coverage** (``ProtMHCPopulationCoverage``): calculates population coverage for a
  set of MHC-I/MHC-II epitopes across selected populations/areas.
- **ElliPro prediction** (``ProtElliProPrediction``): conformational (structural) B-cell epitope
  prediction over an input atomic structure, producing both structure and sequence ROIs.

===============
Buildbot status
===============

Status devel version: 

.. image:: http://scipion-test.cnb.csic.es:9980/badges/bioinformatics_dev.svg

Status production version: 

.. image:: http://scipion-test.cnb.csic.es:9980/badges/bioinformatics_prod.svg
