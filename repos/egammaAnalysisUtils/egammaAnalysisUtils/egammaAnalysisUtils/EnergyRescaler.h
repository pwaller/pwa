//////////////////////////////////////////////////////////////
//DATED: October 23, 2010 
//V0.1
//Author Ashfaq Ahmad <Ashfaq.Ahmad@cern.ch>
//Class to rescale/weight energy of the cluster by applying 
//Calibration Constants.
//for more information please go here
//https://twiki.cern.ch/twiki/bin/view/AtlasProtected/EnergyRescaler
// Jan 26, 2010
//include Nikola Makovec smearing function
//Feb 4, 2010
// include systematics
///////////////////////////////////////////////////////////
#ifndef EnergyRescaler_h
#define EnergyRescaler_h

#include <vector>
#include <string>

#include <TRandom3.h>

#define GeV 1000


class EnergyRescaler {


  

   public:



      EnergyRescaler();
      ~EnergyRescaler();

      ////read text file containing calib constants
      bool readCalibConstants(std::string fname);
      
    
//      typedef enum { NOMINAL=1, ERR_DOWN=2, ERR_UP=3 } CorrType;
      typedef enum { NOMINAL=0, ERR_DOWN=1, ERR_UP=2 } CorrType;


      //take eta/phi and uncorrected energy of electron, return  corrected energy, 
      //last argurment is to choose central/down/up energy corrections, default is nominal/central value
     
      double applyEnergyCorrectionGeV(double cl_eta, double cl_phi, double uncorr_energy, double et, int value=NOMINAL /* NOMINAL=0, ERROR_DOWN==1, ERROR_UP==2*/, std::string part_type="ELECTRON" ) const;

      double applyEnergyCorrectionMeV(double cl_eta, double cl_phi, double uncorr_energy, double et, int value=NOMINAL /* NOMINAL=0, ERROR_DOWN==1, ERROR_UP==2*/, std::string part_type="ELECTRON" ) const;


      //if can't use the above method then use this method to read the default constants(note they are not egamma default constants
      //but for private use only!)

      bool useDefaultCalibConstants(std::string corr_version="2011");


      ///set random seed to some fix value(would need for MC comparison )
      
      void SetRandomSeed(unsigned seed=0 );

      
      ////get smearing correction
      double getSmearingCorrectionGeV(double eta, double energy, int value=NOMINAL, bool mc_withCT=true,std::string corr_version="2011" ) const;
      double getSmearingCorrectionMeV(double eta, double energy, int value=NOMINAL, bool mc_withCT=true,std::string corr_version="2011" ) const;


      ////print the constants
      bool printMap() const;

      //get systematics error, user should not call this method. Use it via applyEnergyCorrection
      void getErrorGeV(double cl_eta,double cl_et, double &er_up, double &er_do, std::string part_type="ELECTRON",bool withXMAT=true,bool withPS=true) const;
      void getErrorMeV(double cl_eta,double cl_et, double &er_up, double &er_do, std::string part_type="ELECTRON",bool withXMAT=true,bool withPS=true) const;
      

   private:
      
      std::string corr_version;

      mutable TRandom3   m_random3;

      struct calibMap { 
 
            double eta; 
            double phi; 
            double etaBinSize; 
            double phiBinSize; 
            double alpha; 
            double alphaErr; 
      }; 


      std::vector< calibMap > corrVec;
 
      
};

inline double EnergyRescaler::applyEnergyCorrectionMeV(double cl_eta, double cl_phi, double uncorr_energy, 
						       double et, int value, std::string part_type) const
{ 
  return applyEnergyCorrectionGeV(cl_eta, cl_phi, uncorr_energy/GeV, et/GeV, value, part_type) * GeV;
}

inline double EnergyRescaler::getSmearingCorrectionMeV(double eta, double energy, int value, bool mc_withCT,std::string corr_version) const
{
  return getSmearingCorrectionGeV(eta, energy/GeV, value, mc_withCT, corr_version);
}

inline void EnergyRescaler::getErrorMeV(double cl_eta,double cl_et, double &er_up, double &er_do, 
					std::string part_type, bool withXMAT,bool withPS) const
{
  getErrorGeV(cl_eta, cl_et/GeV, er_up, er_do, part_type, withXMAT, withPS);
}

#endif

