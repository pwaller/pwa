

#include <vector>
#include <string>
#include <iostream>
#include <cmath>

/*
-----------------------------------------------------------------------
egammaTriggerMatching: computes the macthing between an offline electron and EF object passing a given trigger

authors:   Valerio Dao <valerio.dao@cern.ch>

matching is performed using the 4momentum eta-phi of the trigger object.
Such variables should correspond to:
- track eta and phi in case the electron has a insideout track (majority of the applications)
- cluster eta-phi in case the track is not found [ only for object passing etcut trigger ]
- ???? for TRT only electron ....

-----------------------------------------------------------------------
usage:

COMMENT:
"all the variable need to be passed to the function to have it independent from any specific D3PD
reader framewrok. User will eventually better integrate into his reader class"

PassedTriggerEF(double etaOff, double phiOff, vector<int> *EFdecision, int &EFindex, 
                int nEFObject, vector<float> *EFetaVector, vector<float> *EFphiVector) {


etaOff: eta of the offline candidate (recommended to use trackEta)
etaOff: eta of the offline candidate (recommended to use trackPhi)

EFdecition: D3PD variable corresponding to the trigger you want to use:
trig_EF_el_EF_XXXXXX where XXXXX is the trigger name

nEFObject  : use the D3PD variable trig_EF_el_n
EFetaVector: use the D3PD variable trig_EF_el_eta
EFphiVector: use the D3PD variable trig_EF_el_phi

EFindex : return the index of the matched EF object

..... 
example:

given offI the index of your offline electron
int EFindex;
if ( el_tracketa->at(offI), el_trackphi->at(offI), trig_EF_el_EF_e60_loose, EFindex, 
     trig_EF_el_n, trig_EF_el_eta, trig_EF_el_phi) {
   std::cout << "Offline electron " << offI << " passed EF_e60_loose trigger by matching to EF object: " << EFindex << std::endl;
} 

*/

const double m_triggerDrMatchingCut=0.15;

double GetDPhi(double phi1, double phi2) {
  double deltaPhi=fabs(phi1-phi2);
  if (deltaPhi>M_PI) deltaPhi=2*M_PI-deltaPhi;
  return deltaPhi;
}

bool  PassedTriggerEF(double etaOff, double phiOff, std::vector<int> *EFdecision, int &EFindex, 
		      unsigned int nEFObject, std::vector<float> *EFetaVector, std::vector<float> *EFphiVector) {
  if (nEFObject==0) {
    //std::cout << "No EF object to be tested" << std::endl;
    return false;
  }
  
  // checking consistency
  if (EFdecision==0) {
    std::cout << "ERROR: empty pointer provided for EFdecision .... returning false" << std::endl;
    return false;
  }
  if (EFdecision->size()!=nEFObject) {
    std::cout << "ERROR: mismatch in the size of the EFdecision vector: " << EFdecision->size() << "  --> expected: " <<  nEFObject << std::endl;
    return false;
  }

  if (EFetaVector==0) {
    std::cout << "ERROR: empty pointer provided for EFeta .... returning false" << std::endl;
    return false;
  }
  if (EFetaVector->size()!=nEFObject) {
    std::cout << "ERROR: mismatch in the size of the EFeta vector: " << EFetaVector->size() << "  --> expected: " <<  nEFObject << std::endl;
    return false;
  }

  if (EFphiVector==0) {
    std::cout << "ERROR: empty pointer provided for EFphi .... returning false" << std::endl;
    return false;
  }
  if (EFphiVector->size()!=nEFObject) {
    std::cout << "ERROR: mismatch in the size of the EFphi vector: " << EFphiVector->size() << "  --> expected: " <<  nEFObject << std::endl;
    return false;
  }
  
  double dRMax=100;
  EFindex=-1;
 
  for (unsigned int j=0;j<nEFObject;j++) {
    if ( EFdecision->at(j)==0 ) continue;   
    double etaEF=EFetaVector->at(j);
    double phiEF=EFphiVector->at(j);
    double deltaR=sqrt(pow(GetDPhi(phiEF,phiOff),2)+pow(etaOff-etaEF,2));   
    if ( deltaR<dRMax ) {
      dRMax=deltaR;
      EFindex=j;
    }
  }
  //std::cout <<  "  minimum deltaR is: " << dRMax << std::endl;
 
  if ( dRMax<=m_triggerDrMatchingCut ) {
    //std::cout << "offline object matched with EFobject: " << EFindex << " passing the trigger selection" << std::endl;
    return true;
  } 
  EFindex=-1;
  return false;
}
