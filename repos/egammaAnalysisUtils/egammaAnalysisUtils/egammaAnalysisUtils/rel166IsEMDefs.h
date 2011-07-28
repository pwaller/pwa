#ifndef REL16ISEMDEFS_H
#define REL16ISEMDEFS_H

//----------------------------------------------------------------------------------------

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

namespace rel166{

  //----------------------------------------------------------------------------------------
  bool isLoose(double eta, double eT,
		     double rHad, double rHad1, double Reta, double w2, 
		     bool debug=false);

  //-------------------------------------------------------------------------------------------------------
  bool isMedium(double eta, double eT,
		      double rHad, double rHad1, double Reta, double w2, 
		      double f1, double wstot, double DEmaxs1, double deltaEta, double d0,
		      int nSi, int nPix,
		      bool debug = false );


  //-------------------------------------------------------------------------------------------------------
  bool isTight(double eta, double eT,
	       double rHad, double rHad1, double Reta, double w2, 
	       double f1, double wstot, double DEmaxs1, double deltaEta, double d0,
	       double TRratio, int nTRT, int nTRTOutliers,
	       int nSi, int nPix, double deltaPhi,
	       int nBlayer, bool expectBlayer, int isEM,
	       bool debug = false );


  // Cut Helper Functions 
  bool passRHad(double rHad, double rHad1, unsigned int eTBin, unsigned int etaBin);
  bool passReta(double rEta, unsigned int eTBin, unsigned int etaBin);
  bool passW2(double w2, unsigned int eTBin, unsigned int etaBin);
  bool passWstot(double wstot, unsigned int eTBin, unsigned int etaBin);
  bool passEratio(double DEmaxs1, unsigned int eTBin, unsigned int etaBin);
  bool passEoverP(double EoverP, unsigned int eTBin, unsigned int etaBin);
  // Helper Fuctions
  unsigned int getEtaBin(double eta);
  unsigned int getEtBin(double eT);

}
//----------------------------------------------------------------------------------------
#endif
