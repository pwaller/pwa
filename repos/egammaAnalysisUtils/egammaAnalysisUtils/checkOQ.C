/****************************************************************************************
//
// ROOT macro to apply object-level quality cuts
//

EXAMPLE of how to use:
root -l
    .L checkOQ.C++;
    egammaOQ myOQ;
    myOQ.checkOQClusterPhoton(152209, 0.6, 1.2, false); //(put "true" if converted)
    myOQ.checkOQClusterElectron(152209, -1.4, 2.2);
IF I GET 3 AS OUTPUT I HAVE TO REJECT THE CLUSTER

IMPORTANT NOTE: It is recommended to use the eta and phi of the cluster!

**********************************************************************************/

#include "egammaAnalysisUtils/checkOQ.h"

#include <cmath>
using std::abs;

#include <TMath.h>

//ClassImp(egammaOQ)

egammaOQ::egammaOQ( string /*name*/ )
{
  //TNamed::SetName( name.c_str() );
}

egammaOQ::~egammaOQ()
{
}


//
// Main functions:
// check quality of cluster in run=runnumber, with barycenter (myEta,myPhi),
// either candidate="photon" or "electron"
//

int egammaOQ::checkOQClusterElectron(int runnumber, double myEta, double myPhi, bool syst, bool verbose) const {

  int particletype=1;
  int result=egammaOQ::checkOQCluster(runnumber, myEta, myPhi, particletype, syst, verbose);

  return result;
}

int egammaOQ::checkOQClusterPhoton(int runnumber, double myEta, double myPhi, bool conv, bool syst, bool verbose) const {

  int particletype=2;
  if(conv) particletype=3;
  int result=egammaOQ::checkOQCluster(runnumber, myEta, myPhi, particletype, syst, verbose);

  return result;
}


int egammaOQ::checkOQCluster(int runnumber, double myEta, double myPhi, int candidate, bool syst, bool verbose) const {

  //check that the run is affected
  if (runnumber<180614) {
    return 1;
  }


  //
  // check that user has selected either photon or electron as candidate type
  //
  if ( (candidate!=1) && (candidate!=2) && (candidate!=3)) {
    std::cout << "Wrong candidate type selected: " << candidate << std::endl;
    std::cout << "Please choose either electron(=1) or unconverted photon (=2) or converted photon (=3) or" << std::endl;
    return 3;
  }


  //
  // define cluster size around cluster barycenter
  //
  int netacells=0;
  int nphicells=0;
  int addcell= 0;
  if (syst) addcell=1;
  const double etabarrel=1.37; 
  bool isinbarrel = (abs(myEta) < etabarrel);
  //FOR THE MOMENT WE USE SAME REGIONS
  if (candidate==1) {  //CASE OF ELECTRON
    if (isinbarrel) {
      netacells = 3+addcell;
      nphicells = 7+addcell;
    } else {
      netacells = 5+addcell;
      nphicells = 5+addcell;
    }
  }
  else if (candidate==2) {  // CASE OF UNCONVERTED PHOTON
    if (isinbarrel) {
      netacells = 3+addcell;
      nphicells = 5+addcell;
    } else {
      netacells = 5+addcell;
      nphicells = 5+addcell;
    }
  }
  else if (candidate==3) {  // CASE OF CONVERTED PHOTON
    if (isinbarrel) {
      netacells = 3+addcell;
      nphicells = 7+addcell;
    } else {
      netacells = 5+addcell;
      nphicells = 5+addcell;
    }
  }


  //
  // check quality of cluster
  //
  return checkOQCluster(myEta, myPhi, netacells, nphicells, candidate, verbose);
}


//
// helper function: check cluster defined by barycenter (myEta, myPhi) and cluster size (NetaCells, NphiCells)
//
int egammaOQ::checkOQCluster(double myEta, double myPhi, int NetaCells, int NphiCells, int candidate, bool verbose) const {
  // It returns : 0 if the cluster is ok;
  //              3 if the cluster is bad;

  if (verbose) std::cout << "CHECKING THE " << NetaCells << "x" << NphiCells << " CLUSTER CENTERED IN ===> " << myEta << " " << myPhi << std::endl;   

  double etaCell = myEta;
  double phiCell = myPhi;

  // Check the whole cluster
  //
  if (verbose) std::cout << "checking the whole cluster..." << endl;
  int clusFull =  deadRegionS2(etaCell, phiCell, NetaCells*0.025/2., NphiCells*0.025/2., candidate, verbose);

  return(clusFull);

}




//
// Check for dead regions in S2
//
int egammaOQ::deadRegionS2(double myEta, double myPhi, double deltaEta, double deltaPhi, int /*candidate*/, bool /*verbose*/) const {
  
  int theValue= 0; 
  
  double etaLowBound=myEta-deltaEta;
  double etaUpBound=myEta+deltaEta;
  double phiLowBound=myPhi-deltaPhi; 
  double phiUpBound=myPhi+deltaPhi;
  const double pi = TMath::Pi();
  if(phiLowBound<-pi) phiLowBound +=  2.*pi; //crossing the lower bound in Phi
  if(phiUpBound> pi) phiUpBound -=  2.*pi;  //crossing upper bound in Phi
  
  //4 dead Febs from run 180614:  eta-phi range: [0.0,1.45] x [-0.78847,-0.59213]
  //S2
  if(etaLowBound>=0. && etaLowBound <=1.45) {
    if( phiLowBound>=-0.78847 && phiLowBound<=-0.59213) return 3;
    if( phiUpBound>=-0.78847 && phiUpBound<=-0.59213) return 3;
  }
  if(etaUpBound>=0. && etaUpBound <=1.45) {
    if( phiLowBound>=-0.78847 && phiLowBound<=-0.59213) return 3;
    if( phiUpBound>=-0.78847 && phiUpBound<=-0.59213) return 3;
  }
  
  return(theValue);
}

