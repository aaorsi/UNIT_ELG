# Adam Stevens, 2018
# Functions for reading SAGE data in the format for MultiDark and UNITSIM
import numpy as np
#from pylab import *
import os

def galdtype_multidark():
    # for definitions/units of the fields, see http://multidarkgalaxies.pbworks.com/w/page/100799587/SAGE%20output
    Galdesc_full = [
                    ('SnapNum'                      , np.int32),
                    ('Type'                         , np.int32),
                    ('GalaxyIndex'                  , np.int64),
                    ('CentralGalaxyIndex'           , np.int64),
                    ('CtreesHaloID'                 , np.int64),
                    ('TreeIndex'                    , np.int32),
                    ('CtreesCentralID'              , np.int64),
                    ('mergeType'                    , np.int32),
                    ('mergeIntoID'                  , np.int32),
                    ('mergeIntoSnapNum'             , np.int32),
                    ('dT'                           , np.float32),
                    ('Pos'                          , (np.float32, 3)),
                    ('Vel'                          , (np.float32, 3)),
                    ('Spin'                         , (np.float32, 3)),
                    ('Len'                          , np.int32),
                    ('Mvir'                         , np.float32),
                    ('CentralMvir'                  , np.float32),
                    ('Rvir'                         , np.float32),
                    ('Vvir'                         , np.float32),
                    ('Vmax'                         , np.float32),
                    ('VelDisp'                      , np.float32),
                    ('ColdGas'                      , np.float32),
                    ('StellarMass'                  , np.float32),
                    ('BulgeMass'                    , np.float32),
                    ('HotGas'                       , np.float32),
                    ('EjectedMass'                  , np.float32),
                    ('BlackHoleMass'                , np.float32),
                    ('IntraClusterStars'            , np.float32),
                    ('MetalsColdGas'                , np.float32),
                    ('MetalsStellarMass'            , np.float32),
                    ('MetalsBulgeMass'              , np.float32),
                    ('MetalsHotGas'                 , np.float32),
                    ('MetalsEjectedMass'            , np.float32),
                    ('MetalsIntraClusterStars'      , np.float32),
                    ('SfrDisk'                      , np.float32),
                    ('SfrBulge'                     , np.float32),
                    ('SfrDiskZ'                     , np.float32),
                    ('SfrBulgeZ'                    , np.float32),
                    ('DiskRadius'                   , np.float32),
                    ('Cooling'                      , np.float32),
                    ('Heating'                      , np.float32),
                    ('QuasarModeBHaccretionMass'    , np.float32),
                    ('TimeOfLastMajorMerger'        , np.float32),
                    ('TimeOfLastMinorMerger'        , np.float32),
                    ('OutflowRate'                  , np.float32),
                    ('MeanStarAge'                  , np.float32),
                    ('infallMvir'                   , np.float32),
                    ('infallVvir'                   , np.float32),
                    ('infallVmax'                   , np.float32)
                    ]
    names   = [Galdesc_full[i][0] for i in range(len(Galdesc_full))]
    formats = [Galdesc_full[i][1] for i in range(len(Galdesc_full))]
    Galdesc = np.dtype({'names':names, 'formats':formats}, align=True)
    return Galdesc



def sageoutsingle(fname, fields=[]):
    # Read a single SAGE output file, returning all the galaxy data in a record array
    # fname is the full name for the file to read, including its path
    # fields is the list of fields you want to read in.  If empty, will read all fields.
    Galdesc = galdtype_multidark()
    if len(fields)==0:
        fields=list(Galdesc.names)

    fin      = open(fname, 'rb')                                           # Open the file
    Ntrees   = np.fromfile(fin, np.dtype(np.int32),1)                      # Read number of trees in file
    NtotGals = np.fromfile(fin, np.dtype(np.int32),1)[0]                   # Read number of gals in file.
    
    if NtotGals == 0:
        print('no galaxies in file: ',fname)
    
    if (Ntrees != 0):
        GalsPerTree = np.fromfile(fin, np.dtype((np.int32, Ntrees)),1)     # Read the number of gals in each tree
    G = np.fromfile(fin, Galdesc, NtotGals)                                # Read all the galaxy data       
    G = G[fields]                                                          # Reduce to fields of interest
    return G 



def sagesnap(fpre, filelist, fields=[]):
    # Read full SAGE snapshot, going through each file and compiling into 1 array
    # fpre is the name of the file up until the _ before the file number
    # filelist contains all the file numbers you want to read in
    print('  Loading ',fpre,'_',filelist)

    Galdesc = galdtype_multidark()
    if len(fields)==0:
        fields=list(Galdesc.names)

    # create empty storage for all galaxy properties (will be removed again at the end)
#    G = np.empty(1,dtype=Galdesc)
#    G[:][0] = 0.0 
    G = np.zeros(1,dtype=Galdesc)
       
    # extract fields of interest
    G = G[fields]
    
    # loop over file-extensions given in filelist[]
    for i in filelist:
        fname    = fpre+'_'+str(i)
        filesize = os.path.getsize(fname)

        # capture possibly empty files
        if filesize > 0:
            G1 = sageoutsingle(fname, fields)
            G = np.append(G, G1)

    # remove the first (empty) field again
    G = G[:][1:]

    print('    -> found',len(G[:][:]),' galaxies')
    return G


""" Example code for reading in data, feel free to copy:
    fields = ['StellarMass', 'CtreesHaloID', 'Type', 'Mvir'] # specify whichever fields you want to read here (refer to the names in the first function).  Can leave empty
    files = range(100) # list of file numbers to read.  They don't need to be consecutive.
    fpre = '/data2/users/astevens/SAGE_output/UNITSIM1/model_z0.000' # where the data are stored, what the common string in the files is before the last underscore
    G = sagesnap(fpre, files, fields)
    
    # Then do, e.g. G['StellarMass'] to get the stellar masses of the galaxies.
    
    """

