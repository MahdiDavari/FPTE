# Finite Pressure Temperature Elasticity (FPTE) package
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/MahdiDavari/FPTE?quickstart=1)

<a href="https://ibb.co/gJpS7Js"><img src="https://i.ibb.co/VTZgNTX/Stress-Strain.jpg" alt="Stress-Strain" border="0" /></a>

## Installation

### Dependencies

FPTE requires:

- Python (>= 3.7)
- NumPy (>= 1.16.5)
- Pandas (>= 0.25.3)
- Matplotlib (>= 2.2.4)
- joblib (>= 0.11)

FPTE 1.2.0 and later require Python 3.7 or newer. FPTE 1.1.0 and later require Python 3.4 or
newer.

FPTE plotting capabilities (i.e., functions start with `plot_` and classes end with "Display")
require Matplotlib (>= 2.2.4).

### User installation

If you already have a working installation of numpy and scipy, the easiest way to install FPTE
is using `pip`:

    pip install -U FPTE

or `install from source`:

    git clone https://github.com/MahdiDavari/FPTE
    cd FPTE
    python setup.py install

In order to check your installation you can use:

    python -m pip show FPTE  # to see which version and where FPTE is installed
    python -m pip freeze  # to see all packages installed in the active virtualenv
    python -c "import FPTE; print(FPTE.__version__)"

_Note that in order to avoid potential conflicts with other packages it is strongly recommended
to use a virtual environment (venv)._

## Theory

**Elastic Stifness Coefficients from Stress-Strain Relations:**

According to Hooke's law, the second-rank stress and strain tensors for a slightly deformed
crystal are related by

$$ $$

where the fourth rank tensors c<sub>ijkl</sub> and s<sub>ijkl</sub> are called the elastic
stiffness coefficients and elastic compliance constants respectively. Here we deal with elastic
stiffness coefficients c<sub>ijkl</sub>, which govern the proper stress-strain relations at nite
strain. In general, we can write

$$ $$

where X and x are the coordinates before and after the deformation. There are 81 independent
stiffness coefficients in general; however, this number is reduced to 21 by the requirement of
the complete Voigt symmetry. In Voigt notation (c<sub>ij</sub>), the elastic constants form a
symmetric 6x6 matrix

$$ $$

In single suffix notation (running from 1 to 6), we can also use the matrix representations for
stress and strain

$$ $$
<br>
and

$$ $$

where the stress components are &sigma;<sub>1</sub> = &sigma;<sub>xx</sub> ; &sigma;<sub>2</sub>
= &sigma;<sub>yy</sub> ; &sigma;<sub>3</sub> = &sigma;<sub>zz</sub> ; &sigma;<sub>4</sub> =
&sigma;<sub>yz</sub> ; &sigma;<sub>5</sub> = &sigma;<sub>zx</sub> ; &sigma;<sub>6</sub> =
&sigma;<sub>xy</sub>, and the strain components are &epsilon;<sub>1</sub> = &epsilon;<sub>
xx</sub> ; &epsilon;<sub>2</sub> = &epsilon;<sub>yy</sub> ; &epsilon;<sub>3</sub> =
&epsilon;<sub>zz</sub> ; &epsilon;<sub>4</sub> = &epsilon;<sub>yz</sub> ; &epsilon;<sub>5</sub>
= &epsilon;<sub>zx</sub> ; &epsilon;<sub>6</sub> = &epsilon;<sub>xy</sub>. When a crystal
lattice is deformed with strain (&epsilon;), new lattice vectors a are related to old vectors **
a**<sub>0</sub> by **a** = (I + &epsilon;) **a**<sub>0</sub>, where I is identity matrix. The
stress-strain relations are then simply given by

$$ $$

The presence of the symmetry in the crystal reduces further the number of independent c<sub>
ij</sub> . A cubic crystal having highest symmetry is characterized by the lowest number (only
three) of independent elastic constants, c<sub>11</sub>, c<sub>12</sub> and c<sub>44</sub>,
which in matrix notation is

$$ $$

|      Crystal System          |Space Group Number           |No. of Elastic Constants                         |
|----------------|-------------------------------|-----------------------------|
|`Cubic`|195-230     | 3  |
|`Hexagonal`    |168-194  |5    |
|`Trigonal`     |143-167|6-7|
|`Tetragonal` |75-142 |6-7|
|`Orthorhombic`| 16-74 | 9|
|`Monoclinic` | 3-15| 13|
|`Triclinic` | 1 and 2 | 21|

> **Note:** For **more information** regarding the second-order elastic constant see reference: <br>

1. Golesorkhtabar, Rostam, et al., “ElaStic: A Tool for Calculating Second-Order Elastic
   Constants from First Principles.” Computer Physics Communications 184, no. 8 (2013): 1861–73.

2. Karki, Bijaya B. “High-Pressure Structure and Elasticity of the Major Silicate and Oxide
   Minerals of the Earth’s Lower Mantle,” 1997.

3. Barron, THK, and ML Klein. “Second-Order Elastic Constants of a Solid under Stress.”
   Proceedings of the Physical Society 85, no. 3 (1965): 523.
