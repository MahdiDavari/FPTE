.. -*- mode: rst -*-

|Azure| |CirrusCI| |Codecov| |CircleCI| |Nightly wheels| |Black| |PythonVersion| |PyPi|

.. |Azure| image:: https://dev.azure.com/MDavari/FPTE/_apis/build/status/MahdiDavari.FPTE?branchName=master
   :target: https://dev.azure.com/MDavari/FPTE/_build/latest?definitionId=1&branchName=master

.. |CircleCI| image:: https://circleci.com/gh/MahdiDavari/FPTE/tree/main.svg?style=shield
   :target: https://circleci.com/gh/MahdiDavari/FPTE

.. |CirrusCI| image:: https://img.shields.io/cirrus/github/MahdiDavari/FPTE/main?label=Cirrus%20CI
   :target: https://cirrus-ci.com/github/MahdiDavari/FPTE/main

.. |Codecov| image:: https://codecov.io/gh/MahdiDavari/FPTE/branch/main/graph/badge.svg?token=Pk8G9gg3y9
   :target: https://codecov.io/gh/MahdiDavari/FPTE

.. |Nightly wheels| image:: https://github.com/MahdiDavari/FPTE/workflows/Wheel%20builder/badge.svg?event=schedule
   :target: https://github.com/MahdiDavari/FPTE/actions?query=workflow%3A%22Wheel+builder%22+event%3Aschedule

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/FPTE.svg
   :target: https://pypi.org/project/FPTE

.. |PyPi| image:: https://img.shields.io/pypi/v/FPTE
   :target: https://pypi.org/project/FPTE

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |DOI| image:: https://zenodo.org/badge/21369/MahdiDavari/FPTE.svg
   :target: https://zenodo.org/badge/latestdoi/21369/MahdiDavari/FPTE


.. |PythonMinVersion| replace:: 3.7
.. |NumPyMinVersion| replace:: >=1.16.5
.. |PandasMinVersion| replace:: >=0.25.3
.. |JoblibMinVersion| replace:: >=0.11
.. |MatplotlibMinVersion| replace:: >=2.2.4
.. |PytestMinVersion| replace:: >=7.1.2




.. image:: https://i.ibb.co/VTZgNTX/Stress-Strain.jpg
  :target: https://fpte.org/



Installation
------------

Dependencies
~~~~~~~~~~~~

FPTE requires:

- Python (|PythonMinVersion|)
- NumPy (|NumPyMinVersion|)
- Pandas (|PandasMinVersion|)
- Matplotlib (|MatplotlibMinVersion|)
- joblib (|JoblibMinVersion|)

FPTE 1.2.0 and later require Python |PythonMinVersion| or newer. FPTE 1.1.0 and later require Python 3.4 or
newer.

FPTE plotting capabilities (i.e., functions start with ``plot_`` and classes end with ``Display``)
require Matplotlib |MatplotlibMinVersion| (>= 2.2.4).

User installation
~~~~~~~~~~~~

If you already have a working installation of numpy and scipy, the easiest way to install FPTE
is using ``pip``::

    pip install -U FPTE

or ``install from the source``::

    git clone https://github.com/MahdiDavari/FPTE
    cd FPTE
    pip install -e .

In order to check your installation you can use::

    python -m pip show FPTE  # to see which version and where FPTE is installed
    python -m pip freeze  # to see all packages installed in the active virtualenv
    python -c "import FPTE; print(FPTE.__version__)"

*Note that in order to avoid potential conflicts with other packages it is strongly recommended
to use a virtual environment (venv).*

Theory
------

**Elastic Stiffness Coefficients from Stress-Strain Relations:**

According to Hooke's law, the second-rank stress and strain tensors for a slightly deformed
crystal are related by

.. math::
   \frac{ \sum_{t=0}^{N}f(t,k) }{N}


where the fourth rank tensors :math:`c_{ijkl}` and :math:`s_{ijkl}` are called the elastic
stiffness coefficients and elastic compliance constants respectively. Here we deal with elastic
stiffness coefficients :math:`c_{ijkl}`, which govern the proper stress-strain relations at nite
strain. In general, we can write

.. math::
   \frac{ \sum_{t=0}^{N}f(t,k) }{N}

where :math:`X` and :math:`x` are the coordinates before and after the deformation. There are 81 independent
stiffness coefficients in general; however, this number is reduced to 21 by the requirement of
the complete Voigt symmetry. In Voigt notation ($`c_{ij}`$), the elastic constants form a
symmetric 6x6 matrix

.. math::
   \frac{ \sum_{t=0}^{N}f(t,k) }{N}

In single suffix notation (running from 1 to 6), we can also use the matrix representations for
stress and strain

```math
\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)
```

and

.. math::
   \frac{ \sum_{t=0}^{N}f(t,k) }{N}

where the stress components are :math:`\sigma_1` = :math:`\sigma_xx` ; :math:`\sigma_2`
= :math:`\sigma_yy` ; :math:`\sigma_3` = :math:`\sigma_zz` ; :math:`\sigma_4` =
:math:`\sigma_yz` ; :math:`\sigma_5` = :math:`\sigma_zx` ; :math:`\sigma_6` =
:math:`\sigma_xy`, and the strain components are :math:`\epsilon_1` = :math:`\epsilon_
xx` ; :math:`\epsilon_2` = :math:`\epsilon_yy` ; :math:`\epsilon_3` =
:math:`\epsilon_zz` ; :math:`\epsilon_4` = :math:`\epsilon_yz` ; :math:`\epsilon_5`
= :math:`\epsilon_zx` ; :math:`\epsilon_6` = :math:`\epsilon_xy`. When a crystal
lattice is deformed with strain (:math:`\epsilon`), new lattice vectors a are related to
old vectors :math:`a_0` by :math:`a = (I + \epsilon) a_0`, where :math:`I` is identity matrix.
The stress-strain relations are then simply given by

.. math::
   \frac{ \sum_{t=0}^{N}f(t,k) }{N}

The presence of the symmetry in the crystal reduces further the number of independent :math:`c_
ij` . A cubic crystal having highest symmetry is characterized by the lowest number (only
three) of independent elastic constants, :math:`c_11`, :math:`c_12` and :math:`c_44`,
which in matrix notation is

.. math::
   \frac{ \sum_{t=0}^{N}f(t,k) }{N}


.. list-table:: List of Crystal Systems
   :widths: 40 40 40
   :header-rows: 1

   * - **Crystal System**
     - **Space Group Number**
     - **No. of Elastic Constants**
   * - *Cubic*
     - 195-230
     - 3
   * - *Hexagonal*
     - 168-194
     - 5
   * - *Trigonal*
     - 143-167
     - 6-7
   * - *Tetragonal*
     - 75-142
     - 6-7
   * - *Orthorhombic*
     - 16-74
     - 9
   * - *Monoclinic*
     - 3-15
     - 13
   * - *Triclinic*
     -  1 and 2
     - 21

::

 Note: For **more information** regarding the second-order elastic constant see reference:

.. [1] Golesorkhtabar, Rostam, et al., “ElaStic: A Tool for Calculating Second-Order Elastic
   Constants from First Principles.” Computer Physics Communications 184, no. 8 (2013): 1861–73.
.. [2] Karki, Bijaya B. “High-Pressure Structure and Elasticity of the Major Silicate and Oxide
   Minerals of the Earth’s Lower Mantle,” 1997.
.. [3] Barron, THK, and ML Klein. “Second-Order Elastic Constants of a Solid under Stress.”
   Proceedings of the Physical Society 85, no. 3 (1965): 523.
