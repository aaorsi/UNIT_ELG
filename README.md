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

The function `read_elgs()` has the following arguments:

```p
def read_elgs(dirname, basename, ivol0, ivol1, Properties='all')
```


where `dirname` and `basename` define the base of the filenames (see the exmaple in `read_lines.py`), 
`ivol0`,`ìvol1` corresponds to the subvolumes to be read (0 to 999), and `Properties` can be set to a list
of strings that correspond to specific properties to be included in the output. The default is 'all'. The full list of properties, as of now, is 

`['OII_3727', 'OII_3729', 'CentralMvir', 'Pos', 'OIII_5007', 'Halpha', 'GalaxyIndex', 'Mvir', 'Vel']`

but this can be modified in `fetch_lines.py`. This routine reads files from UNIT Sage, computes emission lines and it outputs those properties from above into a hdf5 file.
