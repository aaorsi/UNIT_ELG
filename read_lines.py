# This routine reads ELG catalgoues produced with fetch_lines.py


import deepdish as dd
import numpy as np

def read_elgs(dirname, basename, ivol0, ivol1, Properties='all'):

  outdict = {}

  for iv in range(ivol0,ivol1):
    ifile = '%s/%s_%d.h5'%(dirname, basename, iv)
    print ifile,
    if Properties == 'all':
      data = dd.io.load(ifile)
    else:
      props = ['/'+p for p in Properties]
      data_t = dd.io.load(ifile, props)
      data = {}
      for i in range(len(Properties)):
        pp = Properties[i]
        data[pp] = data_t[i]


    print len(data['OII_3727'])
    if iv > ivol0:
      for key in data.keys():
        outdict[key] = np.concatenate([outdict[key],data[key]])
    else:
      outdict = data


  return outdict



import multiprocessing as mp

dirname = '/home2/aorsi/UNIT_ELGs/UNITSIM1/'
basename = 'model_z1.032'
props = ['OII_3727', 'OII_3729']

nproc = 10  # number of parallel processes
i0 = 0  # file sub-volumes
i1 = 999

npp = int((i1-i0+1.0)/(nproc+0.0))


def run_readmp(ip):
  iv0 = npp*ip
  iv1 = npp*(ip+1)
  if ip == nproc-1:
    iv1 = i1  # last process is forced to reach the last sub-volume
    
  outdata = read_elgs(dirname, basename,iv0,iv1,Properties=props)
  return outdata


pool = mp.Pool(processes=nproc)
results = [pool.apply(run_readmp, args=(x,)) for x in range(nproc)]

elgs = {}
keys = results[0].keys()

print 'joining all results in one dictionary...'
for k in keys:
  print k
  elgs[k] = np.concatenate([results[i][k] for i in range(len(results))])

print elgs.keys()
print 'Number  of elgs:%d'%len(elgs[keys[0]])


