#ifndef ISEMPLUSPLUSDEFS_H
#define ISEMPLUSPLUSDEFS_H

#include <fstream>
#include <iostream>
//----------------------------------------------------------------------------------------

/**
   Author: John Alison <johnda@sas.upenn.edu>
           Chris Lester <clester@sas.upenn.edu>
	   
   Includes:
         
     Loose++ Optimization for  > 20 GeV electrons (MC corrected from Z T and P)
     Medium++ Optimization for  > 20 GeV electrons (MC corrected from Z T and P)
     Tight++ Optimization for  > 20 GeV electrons (MC corrected from Z T and P)
	    
	   Loose++  Optimization for  10-20 GeV electrons (MC corrected from TightEle)
     Medium++ Optimization for 10-20 GeV electrons (MC corrected from Tight Ele )
	   Tight++ Optimization for 10-20 GeV electrons (MC corrected from Tight Ele )
	   
   Usage:
     The is isTightPlusPlus, isMediumPlusPlus, and isLoosePlusPlus methods take input PiD Variables,
     and returns true if the electron satisfies the loose++ or medium++ requriements.
     It returns false otherwise.

     Additional output will be givedn if debug is set, (false by default).
     
     The trigger bit emulates the online selction of e20_medium1.

     An example of using the macro with the details of the input variables can be found 
       in offline/Reconstruction/egamma/egammaAnalysis/egammaAnalysisUtils

   Created:
      June 2011

*/
//-------------------------------------------------------------------------------------------------------
bool isLoosePlusPlus(double eta, double eT,
		     double rHad, double rHad1, double Reta, double w2,
		     double f1, double wstot, double DEmaxs1, double deltaEta, int nSi,
         int nSiOutliers, int nPix, int nPixOutliers,  bool debug = false,bool isTrigger = false );
  
//-------------------------------------------------------------------------------------------------------
bool isMediumPlusPlus(double eta, double eT,
		      double rHad, double rHad1, double Reta, double w2, 
		      double f1, double wstot, double DEmaxs1, double deltaEta, double d0,
		      double TRratio, int nTRT, int nTRTOutliers,
		      int nSi, int nSiOutliers, int nPix, int nPixOutliers, 
		      int nBlayer, int nBlayerOutliers, bool expectBlayer, 
		      bool debug = false, bool isTrigger = false );
//-------------------------------------------------------------------------------------------------------
bool isTightPlusPlus(double eta, double eT,
		      double rHad, double rHad1, double Reta, double w2, 
		      double f1, double wstot, double DEmaxs1, double deltaEta, double d0,
		      double TRratio, int nTRT, int nTRTOutliers,
		      int nSi, int nSiOutliers, int nPix, int nPixOutliers, 
		      int nBlayer, int nBlayerOutliers, bool expectBlayer,
          double eOverp, double deltaphi, int convBit,   
		      bool debug = false, bool isTrigger = false );


// Loose++ Helper Functions 
bool passRHad_loose(double rhad, double rhad1, unsigned int etbin, unsigned int etabin);
bool passReta_loose(double reta, unsigned int etbin, unsigned int etabin);
bool passW2_loose(double w2, unsigned int etbin, unsigned int etabin);
bool passWstot_loose(double wstot, unsigned int etbin, unsigned int etabin);
bool passEratio_loose(double demaxs1, unsigned int etbin, unsigned int etabin);
bool passDeltaEta_loose(double deltaEta);

// Medium++ Helper Functions 
bool passRHad_med(double rHad, double rHad1, unsigned int eTBin, unsigned int etaBin);
bool passReta_med(double rEta, unsigned int eTBin, unsigned int etaBin);
bool passW2_med(double w2, unsigned int eTBin, unsigned int etaBin);
bool passWstot_med(double wstot, unsigned int eTBin, unsigned int etaBin);
bool passEratio_med(double DEmaxs1, unsigned int eTBin, unsigned int etaBin);
bool passDeltaEta_med(double deltaEta);
bool passTR_med(double TRratio, double eta, unsigned int nTRT);
bool passNPix_med(int nPix, unsigned int etaBin);
bool passNBlayer_med(int nBlayer, unsigned int etaBin); 

// Tight++ Helper Functions 
bool passRHad_tight(double rHad, double rHad1, unsigned int eTBin, unsigned int etaBin);
bool passReta_tight(double rEta, unsigned int eTBin, unsigned int etaBin);
bool passW2_tight(double w2, unsigned int eTBin, unsigned int etaBin);
bool passWstot_tight(double wstot, unsigned int eTBin, unsigned int etaBin);
bool passEratio_tight(double DEmaxs1, unsigned int eTBin, unsigned int etaBin);
bool passTR_tight(double TRratio, double eta, unsigned int nTRT);
bool passNBlayer_tight(int nBlayer, unsigned int etaBin); 
bool passDeltaPhi_tight(double deltaPhi, unsigned int eTBin, unsigned int etaBin); 
bool passEOverP_tight(double eOverp, unsigned int eTBin, unsigned int etaBin); 
bool passNTRT_tight(int nTRT, double eta); 


// Helper Fuctions
unsigned int getEtaBin(double eta);
unsigned int getEtBin(double eT);

//----------------------------------------------------------------------------------------
#endif
