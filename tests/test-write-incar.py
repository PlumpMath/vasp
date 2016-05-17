from nose import *
from vasp import *
import os
from ase import Atom, Atoms

def setup_func():
    "set up test fixtures"
    if os.path.exists('INCAR'):
        os.unlink('INCAR')


def teardown_func():
    "tear down test fixtures"
    if os.path.exists('INCAR'):
        os.unlink('INCAR')


@with_setup(setup_func, teardown_func)
def test0():
    "check ispin"

    atoms = Atoms([Atom('O', [4, 5, 5], magmom=1),
                   Atom('C', [5, 5, 5], magmom=2),
                   Atom('O', [6, 5, 5], magmom=3)],
                   cell=(10, 10, 10))

    calc = Vasp('vasp',
                ispin=2,
                atoms=atoms)

    calc.write_incar('INCAR')

    incar = calc.read_incar('INCAR')

    assert incar['lorbit'] == 11
    assert incar['ispin'] == 2
    assert incar['magmom'] == [1.0, 3.0, 2.0]

    # Now delete it.
    calc.set(ispin=None)
    calc.write_incar('INCAR')

    incar = calc.read_incar('INCAR')
    assert 'ispin' not in incar
    assert 'lorbit' not in incar
    assert 'magmom' not in incar


if __name__ == '__main__':
    test0()