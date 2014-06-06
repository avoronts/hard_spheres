#include <cstdlib>
#include "box.h"
#include <iostream>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#include "vector.h"

//==============================================================
//==============================================================
//  Class Sphere: 
//==============================================================
//==============================================================


//==============================================================
// Constructor
//==============================================================
sphere::sphere()
{
}


//==============================================================
// Constructor
//==============================================================
sphere::sphere(const sphere& s)
{
  i = s.i;
  x = s.x;
  x0 = s.x0;		// !!!!!!!!!!!!  added  by A. Vorontsov
  xns = s.xns;		// !!!!!!!!!!!!  added  by A. Vorontsov
  v  = s.v;
  v0 = s.v0;             // !!!!!!!!!!!!  added  by A. Vorontsov
  cell = s.cell;
  lutime = s.lutime;
  nextevent = s.nextevent;
  nextcollision = s.nextcollision;
}

//==============================================================
// Constructor
//==============================================================
sphere::sphere(int i_i, vector<DIM> x_i, vector<DIM, int> cell_i, double lutime_i):
  i(i_i),
  x(x_i),
  x0(x_i),		// !!!!!!!!!!!!  added  by A. Vorontsov
  xns(x_i),		// !!!!!!!!!!!!  added  by A. Vorontsov
  cell(cell_i),
  lutime(lutime_i)
{
}

//==============================================================
// Destructor
//==============================================================
sphere::~sphere() 
{

}

 
