/****************************************************
Example macro to show the usage of EnergyRescaler 
Author Ashfaq Ahmad <Ashfaq.Ahmad@cern.ch> 
For details see,
https://twiki.cern.ch/twiki/bin/view/AtlasProtected/EnergyRescaler       
****************************************************/

//#include "EnergyRescaler.h"
#include <iostream>

#include <vector>


void useERescaler(){

   ////compile the class
   gROOT->ProcessLine(".L EnergyRescaler.cxx+");
  
   

   
   EnergyRescaler  eRescale;
   eRescale.useDefaultCalibConstants("2011");

   ////print calib constants
   eRescale.printMap();


   //==========================================
   //In case one wants to read scales from text file,(for expert only)
   //formate should be eta/etaBinWidth/phi/phiBinWidth/Alpha/AlphaErrors
   //
   //std::string myfile="Alpha.dat";
   //
   //eRescale.readCalibConstants(myfile);
   //==========================================
   
   //==========================================
   //Define the particle type
   //since energy scale uncertainties are different
   //for electrons, unconverted photons, converted photons
   //==========================================
   std::string part_type="ELECTRON"; //could be ELECTRON, UNCONVERTED_PHOTON, CONVERTED_PHOTON
   //in the current implementation, there is no 
   //difference between converted and unconverted photons

   //==========================================
   //Applying energy scale corrections to data
   //==========================================
   double unCorrE =40.;  // uncorrected calorimetric energy
   double cl_eta=-0.51;  // cluster eta
   double cl_phi=0.;      // cluster phi
   double et=35.;         // et = cl_e/cosh(trk_eta) if (nSCT + nPix) >= 4) otherwise  et = cl_et 
   //==========================================
   //for details on direction recommendation see,
   //https://twiki.cern.ch/twiki/bin/view/AtlasProtected/ElectronsEnergyDirection
   //==========================================

   
   double corrE; 
   ////method returns corrected energy 
   corrE = eRescale.applyEnergyCorrection(cl_eta, cl_phi, unCorrE, et, 0, part_type);
  

   std::cout<<"Uncorrected E : " << unCorrE <<"    corrE : "<<corrE<<std::endl;
   
   //In order to obtained the corrected energy +/- sigma 
   double corrE_down = eRescale.applyEnergyCorrection(cl_eta, 0, unCorrE,et, 1, part_type);
   double corrE_up = eRescale.applyEnergyCorrection(cl_eta, 0, unCorrE,et, 2,  part_type); 
   cout<<corrE_down <<"  "<<corrE<<" "<<corrE_up <<endl;

   //==========================================
   //Uncertainties on the energy scale (to be applied on MC)
   //==========================================
   double cl_e_mc=40;
   double et_mc=40;
   double cl_eta_mc=0;
   double er_up=-1,er_do=-1;
   eRescale.getError(cl_eta_mc,et_mc, er_up, er_do,part_type);
   double energy_up=cl_e_mc*(1+er_up);
   double energy_do=cl_e_mc*(1+er_do);
   cout<<"Energy   : "<<cl_e_mc<<endl;
   cout<<"Energy up: "<<energy_up<<endl;
   cout<<"Energy do: "<<energy_do<<endl;

   //==========================================
   //Applying smearing procedure to MC
   //==========================================
   double energy =40.;

   double smearcorr = 0.;

   double mcWithConstantTerm=true;// if you use a MC without constant term, 
                                  // set this parameter to false otherwise true
   
   ///Set random seed, probably to something like eventNumber+offset
   int evtNumber=65537;
   eRescale.SetRandomSeed(evtNumber);
   

   //// use energy smearing function
   smearcorr = eRescale.getSmearingCorrection(cl_eta, energy, 0, mcWithConstantTerm, "2011");

   cout<<"Energy : "<<energy<<"  Smeared energy : "<< smearcorr*energy<<endl;

   //In order to obtained the smearing corrections +/- sigma 
   double smearcorr_down = eRescale.getSmearingCorrection(cl_eta, energy, 1, mcWithConstantTerm, "2011");
   double smearcorr_up   = eRescale.getSmearingCorrection(cl_eta, energy, 2, mcWithConstantTerm, "2011");


 
}
