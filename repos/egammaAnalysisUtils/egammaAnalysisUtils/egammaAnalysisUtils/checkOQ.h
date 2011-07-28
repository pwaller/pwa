#ifndef egammaOQ_h
#define egammaOQ_h

//#include "TROOT.h"
#include "TString.h"
#include "TFile.h"
#include "TH2I.h"
#include "TNamed.h"

#include <iostream>
#include <string>
#include <map>
#include <vector>

using namespace std;

class egammaOQ {
 
public:

   egammaOQ( string name = "egammaOQ");
   ~egammaOQ();

   int deadRegionS2(double myEta, double myPhi, double deltaEta, double deltaPhi, int candidate, bool verbose=false) const;
   int checkOQCluster(int runnumber, double myEta, double myPhi, int candidate, bool syst=false, bool verbose=false) const;
   int checkOQClusterElectron(int runnumber, double myEta, double myPhi, bool syst=false, bool verbose=false) const;
   int checkOQClusterPhoton(int runnumber, double myEta, double myPhi, bool conv, bool syst=false, bool verbose=false) const;
   int checkOQCluster(double myEta, double myPhi, int NetaCells, int NphiCells, int candidate, bool verbose=false) const;
   

};

#endif
