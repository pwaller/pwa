#include "egammaAnalysisUtils/rel166IsEMDefs.h"
#include "egammaEvent/egammaPIDdefs.h"

#include <iostream>
#include <iomanip>
#include <cmath>

using namespace std;

/**
   Author: John Alison <johnda@sas.upenn.edu>
	   
   Usage:
     The isLoose, isMedium, isTight methods take input PiD Variables,
     and returns true if the electron satisfies the rel 16.6.X isEM cuts

     These cuts were optimized with 2010 data and used in the 2011 data taking.

     This macro's primary purpose is to allow the new cuts to be applied to the 2010 data.
     (which has thus far been reconstructed in 16.0.X) 

     Additional output will be givedn if debug is set, (false by default).
     
   Created:
      May 2011

*/

//----------------------------------------------------------------------------------------
bool rel166::isLoose(double eta, double eT,
		     double rHad, double rHad1, double Reta, double w2, 
		     bool debug
		     ){
		      

  if(eta > 2.47){
    if(debug)
      std::cout << "Failed, eta range. " << std::endl;
    return false;
  }

  unsigned int eTBin = rel166::getEtBin(eT);
  unsigned int etaBin = rel166::getEtaBin(eta);

  // RHad
  if(!rel166::passRHad(rHad,rHad1,eTBin,etaBin)){
    if(debug)
      std::cout << "Failed RHad " << rHad << " rhad1 " << rHad << " " << eT << " " << eta << " " << std::endl;
    return false;
  }

  // Reta 
  if(!rel166::passReta(Reta,eTBin,etaBin)){
    if(debug)
      std::cout << "Failed Reta " << Reta << " " << eT << " " << eta << " " << std::endl;
    return false;
  }

  // w2
  if(!rel166::passW2(w2,eTBin,etaBin)){
    if(debug)
      std::cout << "Failed w2 " << w2 << " " << eT << " " << eta << " " << std::endl;
    return false;
  }

  return true;
}

//-------------------------------------------------------------------------------------------------------
bool rel166::isMedium(double eta, double eT,
		      double rHad, double rHad1, double Reta, double w2, 
		      double f1, double wstot, double DEmaxs1, double deltaEta, double d0,
		      int nSi, int nPix,
		      bool debug ){
		      
  
  if(!rel166::isLoose(eta,eT,rHad,rHad1,Reta,w2,debug)){
    if(debug)
      std::cout << " Failed Loose, so failed Medium" << std::endl;
    return false;
  }

  unsigned int eTBin = rel166::getEtBin(eT);
  unsigned int etaBin = rel166::getEtaBin(eta);

  // Check the energy in the strips before cutting on it
  if(f1 > 0.005){

    // wstot
    if(!rel166::passWstot(wstot,eTBin,etaBin)){
      if(debug)
	std::cout << "Failed wstot " << wstot << " " << eT << " " << eta << " " << std::endl;
      return false;
    }


    // Eratio
    if(!rel166::passEratio(DEmaxs1,eTBin,etaBin)){
      if(debug)
	std::cout << "Failed DEmaxs1 " << DEmaxs1 << " " << eT << " " << eta << " " << f1 << std::endl;
      return false;
    }
  }
  
  // Delta Eta
  if(fabs(deltaEta) > 0.01){
    if(debug)
      std::cout << "Failed dEta " << deltaEta << " " << eT << " " << eta << " " << std::endl;
    return false;
  }

  // Si
  if(nSi < 7){
    if(debug)
      std::cout << "Failed nSi " << nSi << " " << eT << " " << eta << " " << std::endl;
    return false;
  }

  // Pi
  if(nPix < 1){
    if(debug)
      std::cout << "Failed nPi " << nPix << " " << eT << " " << eta << " " << std::endl;
    return false;
  }


  // d0
  if(fabs(d0) > 5){
    if(debug)
      std::cout << "Failed d0 " << d0 << " " << eT << " " << eta << " " << std::endl;
      return false;
  }

  return true;
}



//-------------------------------------------------------------------------------------------------------
bool rel166::isTight(double eta, double eT,
		     double rHad, double rHad1, double Reta, double w2, 
		     double f1, double wstot, double DEmaxs1, double deltaEta, double d0,
		     double TRratio, int nTRT, int nTRTOutliers,
		     int nSi, int nPix, double deltaPhi,
		     int nBlayer, bool expectBlayer, int isEM,
		     bool debug ){

  if(!rel166::isMedium(eta,eT,rHad,rHad1,Reta,w2,f1,wstot,DEmaxs1,deltaEta,d0,nSi,nPix,debug)){
    if(debug)
      std::cout << " Failed Medium, so failed Tight" << std::endl;
    return false;
  }		      

  // Delta Eta
  if(fabs(deltaEta) > 0.005){
    if(debug)
      std::cout << "Failed dEta " << deltaEta << " " << eT << " " << eta << " " << std::endl;
    return false;
  }

  // TR
  bool failTRTCuts = (isEM & egammaPID::TRT_ELECTRON);
  
  if(failTRTCuts){
    if(debug)
      std::cout << "Failed TR  TRratio: " << TRratio 
		<< " nTRT:" << nTRT 
		<< " nTRTOutliers:" << nTRTOutliers 
		<< " Et:" << eT 
		<< " eta:" << eta << " " 
		<< (isEM & egammaPID::TRT_ELECTRON)
		<< std::endl;

    return false;
  }


  // Delta Phi
  if(fabs(deltaPhi) > 0.02){
    if(debug)
      std::cout << "Failed dPhi " << deltaPhi << " " << eT << " " << eta << " " << std::endl;
    return false;
  }
  
  // EoverP 
  bool failsEoverP = (isEM & (0x1 << egammaPID::TrackMatchEoverP_Electron));
  if(failsEoverP){
    if(debug)
      std::cout << "Failed EoverP " << eT << " " << eta << " " << std::endl;
    return false;
  }

  // Blayer
  if(expectBlayer && nBlayer<1){
    if(debug)
      std::cout << "Failed Bl " << nBlayer << " " << eT << " " << eta << " " << std::endl;
    return false;
  }

  // d0
  if(fabs(d0) > 1){
    if(debug)
      std::cout << "Failed d0 " << d0 << " " << eT << " " << eta << " " << std::endl;
    return false;
  }

  bool isConv = (isEM & egammaPID::CONVMATCH_ELECTRON);

  if(isConv){
    if(debug)
      std::cout << "Failed Conversion Bit " << std::endl;
    return false;
  }

  return true;
}

//---------------------------------------------------------------------------------------
// Gets the Eta bin [0-9] given the eta
unsigned int rel166::getEtaBin(double eta){
  const unsigned int nEtaBins = 10;
  const double etaBins[nEtaBins] = {0.1,0.6,0.8,1.15,1.37,1.52,1.81,2.01,2.37,2.47};
  
  for(unsigned int etaBin = 0; etaBin < nEtaBins; ++etaBin){
    if(fabs(eta) < etaBins[etaBin])
      return etaBin;
  }
  
  return 9;
}

//---------------------------------------------------------------------------------------
// Gets the Et bin [0-10] given the et (MeV)
unsigned int rel166::getEtBin(double eT){
  const unsigned int nEtBins = 11;
  const double GeV = 1000;
  const double eTBins[nEtBins] = {5*GeV,10*GeV,15*GeV,20*GeV,30*GeV,40*GeV,50*GeV,60*GeV,70*GeV,80*GeV};
  
  for(unsigned int eTBin = 0; eTBin < nEtBins; ++eTBin){
    if(eT < eTBins[eTBin])
      return eTBin;
  }
  
  return 10;
}

//----------------------------------------------------------------------------------------
bool rel166::passRHad(double rHad, double rHad1,unsigned int eTBin,unsigned int etaBin){


  // New values cut on rHad (rows are eT bins, columns are eta bins)
  //                               0.0   0.1    0.6    0.8   1.15   1.37   1.52   1.81   2.01  2.37    2.47
  const float cutRHad[11][10]  = {{ 0.031, 0.031, 0.021, 0.021, 0.019, 0.028, 0.065, 0.065, 0.046, 0.034}// < 5
				  ,{0.018, 0.018, 0.016, 0.015, 0.016, 0.028, 0.053, 0.038, 0.028, 0.025} // 5-10 
				  ,{0.015, 0.015, 0.014, 0.014, 0.016, 0.020, 0.039, 0.032, 0.027, 0.023}// 10-15 
      				  ,{0.012, 0.012, 0.010, 0.010, 0.012, 0.015, 0.029, 0.022, 0.015, 0.021}// 15-20 
				  ,{0.010, 0.010, 0.010, 0.010, 0.010, 0.010, 0.020, 0.015, 0.014, 0.014}// 20-30 
				  ,{0.008, 0.008, 0.008, 0.008, 0.008, 0.010, 0.014, 0.015, 0.010, 0.010}// 30-40 
				  ,{0.008, 0.008, 0.008, 0.008, 0.008, 0.010, 0.015, 0.015, 0.010, 0.010}// 40-50 
				  ,{0.008, 0.008, 0.008, 0.008, 0.008, 0.010, 0.015, 0.015, 0.010, 0.010}// 50-60 
				  ,{0.008, 0.008, 0.008, 0.008, 0.008, 0.010, 0.015, 0.015, 0.010, 0.010}// 60-70 
				  ,{0.008, 0.008, 0.008, 0.008, 0.008, 0.010, 0.015, 0.015, 0.010, 0.010}// 70-80 
				  ,{0.008, 0.008, 0.008, 0.008, 0.008, 0.010, 0.015, 0.015, 0.010, 0.010}};// 80< 

  if(etaBin == 3 || etaBin == 4){
    if (rHad > cutRHad[eTBin][etaBin])
      return false;
  } else{
    if(rHad1 > cutRHad[eTBin][etaBin])
      return false;
  }

  return true;
}

//----------------------------------------------------------------------------------------
bool rel166::passReta(double rEta, unsigned int eTBin, unsigned int etaBin){
  
  // New values cut on ratio e237/e277 (rows are eT bins, columns are eta bins)
  //                               0.0   0.1    0.6    0.8   1.15   1.37   1.52   1.81    2.01   2.37   2.47
  const float cutReta37[11][10] = {{ 0.700, 0.700, 0.700, 0.700, 0.700, 0.690, 0.848, 0.876, 0.870, 0.888}  // < 5
				   ,{0.700, 0.700, 0.700, 0.700, 0.700, 0.715, 0.860, 0.880, 0.880, 0.880} // 5-10
				   ,{0.860, 0.860, 0.860, 0.860, 0.860, 0.730, 0.860, 0.880, 0.880, 0.880}// 10-15
				   ,{0.860, 0.860, 0.860, 0.860, 0.860, 0.740, 0.860, 0.880, 0.880, 0.880}// 15-20
				   ,{0.930, 0.930, 0.930, 0.925, 0.925, 0.750, 0.915, 0.915, 0.900, 0.900}// 20-30
				   ,{0.930, 0.930, 0.930, 0.925, 0.925, 0.790, 0.915, 0.920, 0.900, 0.900}// 30-40
				   ,{0.930, 0.930, 0.930, 0.925, 0.925, 0.790, 0.915, 0.920, 0.900, 0.900}// 40-50
				   ,{0.930, 0.930, 0.930, 0.930, 0.925, 0.790, 0.915, 0.920, 0.900, 0.900}// 50-60
				   ,{0.930, 0.930, 0.930, 0.930, 0.925, 0.790, 0.915, 0.920, 0.900, 0.900}// 60-70
				   ,{0.930, 0.930, 0.930, 0.930, 0.925, 0.790, 0.915, 0.920, 0.900, 0.900}// 70-80
				   ,{0.930, 0.930, 0.930, 0.930, 0.925, 0.790, 0.915, 0.920, 0.900, 0.900}};// 80<


  if(rEta < cutReta37[eTBin][etaBin])
    return false;

  return true;
}

//----------------------------------------------------------------------------------------
bool rel166::passW2(double w2, unsigned int eTBin, unsigned int etaBin){

  //New values for cut on shower width in 2nd sampling (rows are eT bins, columns are eta bins)
  //                               0.0   0.1    0.6    0.8   1.15   1.37   1.52   1.81    2.01   2.37   2.47
  const float cutWeta2[11][10] = {{ 0.014, 0.014, 0.014, 0.014, 0.014, 0.028, 0.017, 0.014, 0.014, 0.014}   // < 5 
				  ,{0.013, 0.013, 0.014, 0.014, 0.014, 0.026, 0.017, 0.014, 0.014, 0.014}  // 5-10
				  ,{0.013, 0.013, 0.014, 0.014, 0.014, 0.025, 0.017, 0.014, 0.014, 0.014} // 10-15
				  ,{0.012, 0.012, 0.013, 0.013, 0.013, 0.025, 0.017, 0.014, 0.014, 0.014} // 15-20
				  ,{0.011, 0.011, 0.012, 0.012, 0.013, 0.025, 0.014, 0.013, 0.013, 0.013} // 20-30
				  ,{0.011, 0.011, 0.012, 0.012, 0.012, 0.025, 0.013, 0.013, 0.013, 0.013} // 30-40
				  ,{0.011, 0.011, 0.012, 0.012, 0.012, 0.025, 0.013, 0.013, 0.013, 0.013} // 40-50
				  ,{0.011, 0.011, 0.012, 0.012, 0.012, 0.025, 0.013, 0.012, 0.013, 0.013} // 50-60
				  ,{0.011, 0.011, 0.012, 0.012, 0.012, 0.025, 0.013, 0.012, 0.013, 0.013} // 60-70
				  ,{0.011, 0.011, 0.012, 0.012, 0.012, 0.025, 0.013, 0.012, 0.013, 0.013} // 70-80
				  ,{0.011, 0.011, 0.012, 0.012, 0.012, 0.025, 0.013, 0.012, 0.013, 0.013}}; // 80<  

  if(w2 > cutWeta2[eTBin][etaBin])
    return false;
    
  return  true;
}

//----------------------------------------------------------------------------------------
bool rel166::passWstot(double wstot, unsigned int eTBin, unsigned int etaBin){
  // cut on total width in 1st sampling
  //                               0.0   0.1  0.6   0.8   1.15   1.37  1.52  1.81  2.01  2.37  2.47
  const double cutWstot[11][10]  = {{3.48, 3.48, 3.78, 3.96, 4.20, 9999., 4.02, 2.70, 1.86,  9999.} // < 5    GeV
				    ,{3.18, 3.18, 3.54, 3.90, 4.02, 9999., 3.96, 2.70, 1.80,  9999.} // 5-10   
				    ,{2.81, 2.81, 2.97, 3.36, 3.48, 9999., 3.72, 2.42, 1.76,  9999.} // 10-15 
				    ,{2.76, 2.76, 2.92, 3.24, 3.41, 9999., 3.67, 2.35, 1.72,  9999.} // 15-20 
				    ,{2.50, 2.50, 2.70, 3.14, 3.23, 9999., 3.58, 2.32, 1.59,  9999.} // 20-30 
				    ,{2.45, 2.45, 2.70, 2.98, 3.17, 9999., 3.52, 2.25, 1.58,  9999.} // 30-40 
				    ,{2.27, 2.27, 2.61, 2.90, 3.17, 9999., 3.36, 2.25, 1.55,  9999.} // 40-50 
				    ,{2.27, 2.27, 2.61, 2.90, 3.17, 9999., 3.36, 2.25, 1.55,  9999.} // 50-60 
				    ,{2.27, 2.27, 2.61, 2.90, 3.17, 9999., 3.36, 2.25, 1.55,  9999.} // 60-70 
				    ,{2.27, 2.27, 2.61, 2.90, 3.17, 9999., 3.36, 2.25, 1.55,  9999.} // 70-80 
				    ,{2.27, 2.27, 2.61, 2.90, 3.17, 9999., 3.36, 2.25, 1.55,  9999.}}; // 80<   
  

  if(wstot > cutWstot[eTBin][etaBin])
    return false;
    
  return  true;
}

//----------------------------------------------------------------------------------------
bool rel166::passEratio(double DEmaxs1, unsigned int eTBin, unsigned int etaBin){
  
  //cut on (Emax - Emax2)/(Emax + Emax2) in 1st sampling 
  //                               0.0   0.1    0.6    0.8   1.15   1.37   1.52   1.81    2.01   2.37   2.47
  const float cutDEmaxs1[11][10] = {{0.39,  0.39,  0.20,  0.07, 0.06,  -9999.,  0.07,  0.43,   0.75,  -9999.} // < 5  
				    ,{0.61, 0.61,  0.32,  0.11, 0.13,  -9999.,  0.12,  0.51,   0.62,  -9999.} // 5-10  
				    ,{0.67, 0.67,  0.61,  0.43, 0.32,  -9999.,  0.36,  0.82 ,  0.82,  -9999.} // 10-15 
				    ,{0.75, 0.75,  0.67,  0.51, 0.47,  -9999.,  0.43,  0.86 ,  0.84,  -9999.} // 15-20  
				    ,{0.835, 0.835,  0.835,  0.73, 0.70,  -9999.,  0.8,  0.9 ,  0.9,  -9999.} // 20-30  
				    ,{0.835, 0.835,  0.835,  0.73, 0.70,  -9999.,  0.8,  0.9 ,  0.9,  -9999.} // 30-40  
				    ,{0.835, 0.835,  0.835,  0.73, 0.70,  -9999.,  0.8,  0.9 ,  0.9,  -9999.} // 40-50  
				    ,{0.835, 0.835,  0.835,  0.73, 0.70,  -9999.,  0.8,  0.9 ,  0.9,  -9999.} // 50-60  
				    ,{0.835, 0.835,  0.835,  0.73, 0.70,  -9999.,  0.8,  0.9 ,  0.9,  -9999.} // 60-70  
				    ,{0.835, 0.835,  0.835,  0.73, 0.70,  -9999.,  0.8,  0.9 ,  0.9,  -9999.} // 70-80  
				    ,{0.835, 0.835,  0.835,  0.73, 0.70,  -9999.,  0.8,  0.9 ,  0.9,  -9999.}}; // 80<  
  

  if(DEmaxs1 < cutDEmaxs1[eTBin][etaBin])
    return false;
    
  return  true;
}








