# Overview file

#import python classes
import numpy as np
import random as rn
import math
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D
import sys



#import self produced classes
import forcemodule as fm
import init_sys
import correlationmodule

#flags
corrflag = 2

# independent parameters
dt = 0.004
N=108
lpnum = 1000
cutoff = int(lpnum/5.)
density = 0.88
temp = 0.8
Ttarg = 1
Kb =  1
nbins = 100 #number of radial shells
n = 20 #number of timesteps per timeblock in pressure calculation


# Loading initial conditions
mom = init_sys.init_mom(N, temp) 
pos, l, npdim = init_sys.init_pos(N, density) 
forces = init_sys.init_forc(N)
distances = init_sys.init_dist(N)
bin_vec_tot, finalbins = init_sys.init_bins(nbins,lpnum)
toten = init_sys.init_toten(lpnum)
prestime = init_sys.init_presvirialtime(lpnum-cutoff)
kenarray = init_sys.init_kenarray(lpnum)


# Iteration Verlet method
  # Initializing the first values for the loop
pot = 0.0
presvirial = 0.0
forces, pot, distances, presvirial = fm.calc_forces(pos,forces,pot,l,distances,presvirial,[N])
lamda=0
cnt = 0

for lp in range(lpnum):
  mom = mom + forces*0.5*dt
  pos = (pos + mom*dt) % l           # % l means modulo of l, hence it adds/subtracts n*l untill 0<pos<l
  forces, pot, distances, presvirial = fm.calc_forces(pos,forces,pot,l,distances, presvirial, [N])
  mom = mom + forces*0.5*dt
  Ken = np.sum(mom*mom*0.5)
  kenarray[lp,:] = Ken
  toten[lp,:] = Ken + pot
    #print Ken, pot, Ken+pot
  if lp < (cutoff):
    if lp % 10 == 0:
      lamda = np.sqrt((Ttarg*3.*(N-1.)*Kb)/(np.sum(Ken)*2.))
      mom = mom*lamda
  elif corrflag == 1:
    corrflag = 0
    bin_vec_tot = bin_vec_tot + correlationmodule.cor(npdim,N,distances,nbins,finalbins,corrflag)
    corrflag = 1
  elif corrflag ==2:
    prestime[cnt,:] = density*((2*Ken/(3*N)) + presvirial/(3*N) + np.pi*N*0.97596/Ken) 
    cnt = cnt + 1


averagedp = np.zeros((lpnum-cutoff)/n, dtype=float)
for p in range((lpnum-cutoff)/n):
  averagedp[p] = np.mean(prestime[n*p:n*(p+1)])




#fig1 = plt.plot(kenarray)
#fig2 = plt.plot(toten)
#fig3 = plt.plot(toten-kenarray)
fig4 = plt.plot(averagedp)
plt.show()

print min(prestime), max(prestime)

mnp = np.mean(prestime)
sdomp = np.std(prestime)/np.sqrt(len(prestime))
mnavp = sum(averagedp)/len(averagedp)
sdomavp = np.std(averagedp)/np.sqrt(len(averagedp))

print mnp, sdomp, mnavp, sdomavp

#print toten

# Calculate and plot correlationfunction
if corrflag == 1:
  finalbins = 2*bin_vec_tot/((lpnum - cutoff)*density*(N-1))
  bin_vec = correlationmodule.cor(npdim,N,distances,nbins,finalbins,corrflag)


























#  print sum(Ken), sum(pot)[0], toten[0]#, np.sum(mom)
# Plotting the positions



'''
  fig = pylab.figure()
  ax = Axes3D(fig) 
  ax.scatter(pos[:,0],pos[:,1],pos[:,2],c='b')
  ax.set_xlabel('X Label')
  ax.set_ylabel('Y Label')
  ax.set_zlabel('Z Label')
  plt.show()
 '''
