#!/usr/bin/env python
# __*__ coding: utf8 __*__
#!/usr/bin/python 
#==============================================================================
import os
try:
   home_dir=os.environ['HOME']
except:
   home_dir='e:'

import sys
sys.path += [home_dir+'/bin/model/']
sys.path += [home_dir+'/bin/utils/']
sys.path += [os.getcwd()]

#############################################################################
def subst_vars(template,out='in.1',repl={}):
    """Make output file from template by replacing words according to dictionary

    Args:

     template (string): template file name  

     out (string): out file name  

     repl (dict): replace dictionary 
    """
    f=open(out,'w')
    for i in open(template,'r'):
        d=i.split()
        try:
          if d[0]=='variable' and d[2]=='equal' and repl.has_key(d[1]):
            i='variable %s equal %s \n'%(d[1],repl[d[1]])
        except:
          pass
        f.write(i)     
    f.close()

#############################################################################

from dump import dump_lmp
from timer_my import timer_my  as timer
#import numpy as np
from model_voronoi import model_voronoi as model

#############################################################################
#-----------------------------------
def cl(mod):
    sim=mod.vertexes
    ngbr=[[] for i in mod.vertexes]
    for ed in mod.edges:
      v1=ed[3]
      v2=ed[4]
      d2=sum((i-j)**2 for i,j in zip(sim[v1][4:7],sim[v2][4:7]))
      if d2**0.5-sim[v1][7]-sim[v2][7]<0:
         ngbr[v1].append(v2)
         ngbr[v2].append(v1)

    max_color=0
    color=[-1 for i in sim]
    clust=[]
    for i in range(len(sim)):
       at=sim[i]
       if color[i]==-1: 
          c=max_color
          color[i] = c
          max_color +=1
          clust.append([i])
       else:
          c=color[i]

       for ng in ngbr[i]: 
         b=color[ng]
         if b==-1:
           clust[c].append(ng)
           color[ng]=c
         else:
           if b<c:
             for ii in clust[c]:
               color[ii]=b
             clust[b] +=clust[c]
             clust[c]=[]
           if c<b:
             for ii in clust[b]:
               color[ii]=c
             clust[c] +=clust[b]
             clust[b]=[]
  
#    nkl=[len(clust[color[i]])  for i in range(len(sim))]
    clust1=[]
    for i in clust:
      if len(i)>1: clust1.append(i)
    return clust1
###################################

# lists of densities and temperatures

rhol=[1.44+0.01*i for i in range(30)]
templ=[1.5]

for Temp in templ:
    for Rho in rhol:
        v={'Rho':Rho,'Temp':Temp}
        name = '%stm%s'%(str(Rho).rstrip('0.'),str(Temp).rstrip('0.'))
        subst_vars('template.lj',out='in.1',repl=v)
        os.system('lmp_win_no-mpi.exe < in.1')
 
        fil='dump%s.lmp'%(name) 
        print fil
	
        mod=model(dump_lmp(fil)())
        mod.make_verlet(2)
        mod.make_ngbr_new(5,'ne')
        rad=mod.make_radii()
        v=sum([4.*3.1415/3*i**3 for i in rad])
        v1=mod.vc[0]**3
        packing =v/v1 
        mod.add_prop(rad,leg_st='rad',for_st='f')
        mod.make_medvedev('123')

#  rp=[i[7]+0.1 for i in mod.vertexes]
#  print min(rad),max(rp)
#  fil=open('delone.dat','ab')
#  fil.write(str(Rho)+' '+str(Temp)+' '+' %f %f\n'%(2*min(rad),max(rp)))
#  fil.close()

  #      clust=cl(mod)
  #      clm=max(len(i) for i in clust)

        nn=mod.npar()
        print Rho,packing,nn 
        fil=open('por.dat','ab')
        fil.write(str(Rho)+' '+str(Temp)+' '+str(packing)+' %f %f %f %f %f\n'%nn)
        fil.close()
	