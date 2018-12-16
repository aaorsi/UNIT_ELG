#!/usr/bin/env python

import os
import numpy as np
#import allresults as sage
import deepdish as dd
import get_emlines as lines

import read_sage_MDUS as sage
#G = rs.sagesnap(filename, range(1000))
print 'wtf' 

#res = sage.Results()
z = '1.032'

snaplist = [0,999]
nsnap = snaplist[1] - snaplist[0] + 1
#nsnap = 2
bins = 1

Simulation = 'UNITSIM1'

SimDir = '/home/aknebe/Projects/UNITSIM/SAMs/SAGE/%s/'%Simulation
SimName= 'model_z%s'%z

LineFile = './%s/%s' % (Simulation, SimName)


LineNames= ['OII_3727',
            'OII_3729',
            'OIII_5007',
            'Halpha']

IDGals = ['GalaxyIndex']#,'CentralGalaxyIndex','SAGEHaloIndex',
         # 'SAGETreeIndex','SimulationHaloIndex']

PropGals = ['Pos','Vel','Mvir','CentralMvir']

def lumt(lname,gg):
  nzd =  (gg.SfrDiskZ > 0) & (gg.SfrDisk > 0)
  nzb = (gg.SfrBulgeZ > 0) & (gg.SfrBulge > 0)
  ncond = len(nzd)

  lumC = np.zeros(ncond)
  idd = 0
  idb = 0
  for i in range(ncond):
    if nzd[i]:
      lumC[i]+= ldisk_C[lname][idd]
      idd += 1
    if nzb[i]:
      lumC[i]+= lburst_C[lname][idb]
      idb += 1

  return lumC



for i in range(nsnap):

  gfile = SimDir + SimName
  print gfile,i
  #g = sage.sagesnap(gfile, range(i,i))
  g = sage.sageoutsingle("%s_%d"%(gfile,i))
  g = g.view(np.recarray)

  #G = rs.sagesnap(filename, range(1000))
  nzd =  (g.SfrDiskZ > 0) & (g.SfrDisk > 0)
  nzb = (g.SfrBulgeZ > 0) & (g.SfrBulge > 0)
  ldisk_C = lines.get_emlines(g.SfrDisk[nzd], g.SfrDiskZ[nzd], verbose=False)
  lburst_C = lines.get_emlines(g.SfrBulge[nzb], g.SfrBulgeZ[nzb], verbose=False)

  L_Lines= {}
  for lname in LineNames:
    L_Lines[lname] = lumt(lname, g)

  for idg in IDGals:
    L_Lines[idg] = getattr(g,idg)

  for pgal in PropGals:
    L_Lines[pgal] = getattr(g,pgal)

  LineFile_i = '%s_%d.h5'%(LineFile, i)
  
  dd.io.save(LineFile_i,L_Lines)



