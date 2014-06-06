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
#################################################################################
def subst_vars1(template,out='in.1',repl={}):
    """Make output file from template by replacing words according to dictionary

    Args:

     template (string): template file name  

     out (string): out file name  

     repl (dict): replace dictionary 
    """
    data = open(template,'r').read()
    for i in repl:
        str1 = '${%s}'%i
        str2 = str(repl[i])
        data=data.replace(str1,str2)

    f=open(out,'w')
    f.write(data)     
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

rhol=[0.11+0.01*i for i in range(62)]
templ=[1.5]

for Temp in templ:
    for Rho in rhol:
        v={'pf':Rho,'st':1e-5/Rho}
        name = '%stm%s'%(str(Rho).rstrip('0.'),str(Temp).rstrip('0.'))
        subst_vars1('template.hs',out='prepare.in',repl=v)
        os.system('./spheres prepare.in')
        os.system('./spheres stat.in')
 
	f=open('stat.dat','r')
        ln=[i.strip().split() for i in f.readlines()]
        f.close()
        msd=[]
        pf=float(ln[0][0])
        for i in ln:
	    try:
		msd.append(float(i[4])) 
	    except:
		pass
	sxy=0
	sx=0
	sy=0
	sxx=0

        for i,j in enumerate(msd):
	    sxy += i*j
	    sx  += i
	    sy  += j
	    sxx += i*i
	b = (sxy-sx*sy)/(sxx-sx*sx)
	a = (sy - b*sx)/len(msd)


        fil=open('msd.dat','ab')
        fil.write(str(pf)+'  '+str(a)+' '+str(b)+' '+str(sy/len(msd))+'\n' )
        fil.close()
	