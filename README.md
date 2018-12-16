# UNIT_ELG
routines to calculate and analyse ELGs from UNIT simulations

File `read_lines.py` contains a routine to read all hdf5 files containing emission lines for each SAGE galaxy.
When running `read_lines.py`, you should obtain something like this in the end:

````
joining all results in one dictionary...
OII_3729
OII_3727
['OII_3729', 'OII_3727']
Number  of elgs:180892361
````

`read_lines.py` makes use of `deepdish` to read portions of the input hdf5 files (it can be easily installed with `pip`), and `multiprocessing` to read files in many processors at once.

