#ifndef fwdISEMdefs_H_
#define fwdISEMdefs_H_

#include <iostream>
#include <iomanip>
#include <cmath>

/**
Author: Mohamed Aharrouche

functions to get the optimised forward isem definitions.
These definitions are in the default reconstruction since release 16.6

to use the function below : 
-optimised forward loose isem: isOptimisedFwdLoose
-optimised forward loose isem: isOptimisedFwdTight

as input you will need the cluster moments associated to forward electrons.
They are named in D3PD like this:

el_cellmaxfrac 
el_longitudinal
el_secondlambda
el_lateral
el_secondR 
el_centerlambda 


*/

bool isOptimisedFwdLoose(float eta, float centerlambda, float secondlambda, float secondR);
bool isOptimisedFwdTight(float eta, float centerlambda, float secondlambda, float secondR, float longitudinal, float lateral, float cellmaxfrac);

bool isRobustFrwdLoose(float eta, float eT, float SecondLambda, float SecondR, float CenterLambda, float FMax = 0, float longitudinal = 0, float lateral = 0);
bool isRobustFrwdTight(float eta, float eT, float SecondLambda, float SecondR, float CenterLambda, float FMax, float longitudinal, float lateral);



//----------------------------------------------------------------------------------------

double m_centerLambdaCuts[2] = { 280, 280};
double m_secondLambdaCuts[2] = {6000,7300};
double m_secondRCuts[2]      = {2600,1000};
double m_longitudinalCuts[2] = {0.22,0.3 };
double m_lateralCuts[2]      = {0.57,0.3 };
double m_fracMaxCuts[2]      = {0.39,0.45};

//----------------------------------------------------------------------------------------



bool isOptimisedFwdLoose(float eta, float centerlambda, float secondlambda, float secondR) {
  return isRobustFrwdLoose(eta,0,secondlambda,secondR,centerlambda);
}

bool isOptimisedFwdTight(float eta, float centerlambda, float secondlambda, float secondR, float longi, float lat, float cmf) {
  return isRobustFrwdTight(eta,0,secondlambda,secondR,centerlambda,cmf,longi,lat);
}


bool isRobustFrwdLoose(float eta, float eT, float SecondLambda, float SecondR, float CenterLambda, float, float, float){

  int idx = -1;

  if (fabs(eta) > 2.5 && fabs(eta) < 3.2) idx=0;
  else if (fabs(eta) > 3.2 && fabs(eta) < 4.9) idx=1;
  else {
    std::cout << "no valid eta region..." << std::endl;
    return false;
  }

  if (CenterLambda < m_centerLambdaCuts[idx] && SecondLambda < m_secondLambdaCuts[idx] && SecondR < m_secondRCuts[idx])
    return true;
  else
	  return false;

}

bool isRobustFrwdTight(float eta, float eT, float SecondLambda, float SecondR, float CenterLambda, float FMax, float longitudinal, float lateral){

  // If not robustLoose, then not robustMedium
  if(!isRobustFrwdLoose(eta, eT, SecondLambda, SecondR, CenterLambda))
    return false;

  int idx = -1;

  if (fabs(eta) > 2.5 && fabs(eta) < 3.2) idx=0;
  else if (fabs(eta) > 3.2 && fabs(eta) < 4.9) idx=1;

  if (longitudinal < m_longitudinalCuts[idx] && lateral < m_lateralCuts[idx] && FMax > m_fracMaxCuts[idx] )
    return true;
  else
    return false;

}


#endif
