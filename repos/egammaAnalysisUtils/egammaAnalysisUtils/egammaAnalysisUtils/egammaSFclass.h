//Efficiency scale factors macro
//Date: 11/01/2010
//Author: Olivier Arnaez <olivier.arnaez@cern.ch>
//
//float myscalefactortoapply = objsf->scaleFactor(η(cluster), ET(MeV), set, range, rel, etcorrection) 
//returns the combined (W/Z) scale factor and uncertainty vs eta and ET (in MeV) for the egamma
//standard sets of cuts Loose (set=0), Medium (set=1) and Tight (set=2) and for trigger efficiencies
//(set=3) and reco+trkqual efficiencies (set=4) in release 15 (rel=0) / release 16 (rel=1)  / release 
//16.6 estimated from 2010 data (rel=2) / release 16.6 estimated from 2011 data "EPS recommendations" (rel=3)
// / release 16.6 estimated from 2011 data "EPS recommendations" including Jpsi measurements (rel=4)
//measured with probes in the 20-50 GeV range (range=0) or 30-50 GeV (range=1) and correcting (etcorrection=1)
//or not (etcorrection=0) for the ET-dependence
//
//Note that for the most recent sets (EPS recommendations and later), the eta binning is finer and only
//the 20-50 GeV values are provided.
//
//The first number returned is the efficiency scale factor while the second number is
//its uncertainty
//

#ifndef egammaSFclass_h
#define egammaSFclass_h

#include <iostream>
#include <string>
#include <map>
#include <vector>

using namespace std;

class egammaSFclass {

public:

  egammaSFclass();
  ~egammaSFclass() {};

  std::pair<float,float> etCorrection(float ET, int set, int rel=4);
  std::pair<float,float> scaleFactor(float eta, float ET, int set, int range=0, int rel=4, bool etcorrection=true);
  std::pair<float,float> scaleFactorLoose(float eta, float ET=20000., int range=0, int rel=4, bool etcorrection=false) { return scaleFactor(eta, ET, 0, range, rel, etcorrection); };
  std::pair<float,float> scaleFactorMedium(float eta, float ET=20000., int range=0, int rel=4, bool etcorrection=false) { return scaleFactor(eta, ET, 1, range, rel, etcorrection); };
  std::pair<float,float> scaleFactorTight(float eta, float ET=20000., int range=0, int rel=4, bool etcorrection=false) { return scaleFactor(eta, ET, 2, range, rel, etcorrection); };
  std::pair<float,float> scaleFactorTrigger(float eta, float ET=20000., int range=0, int rel=4, bool etcorrection=false) { return scaleFactor(eta, ET, 3, range, rel, etcorrection); };
  std::pair<float,float> scaleFactorRecoTrkQual(float eta, float ET, int range=0, int rel=4, bool etcorrection=false) { return scaleFactor(eta, ET, 4, range, rel, etcorrection); };
  std::pair<float,float> scaleFactorMediumETcorrected(float eta, float ET, int rel=4) { return scaleFactorMedium(eta, ET, 0, rel, true); };
  std::pair<float,float> scaleFactorTightETcorrected(float eta, float ET, int rel=4) { return scaleFactorTight(eta, ET, 0, rel, true); };


  //For the binning
  int m_nEtabins;
  std::vector<float> m_Etabins;
  int m_nETbins;
  std::vector<float> m_ETbins;
  int m_nFineEtabins;
  std::vector<float> m_FineEtabins;
  int m_nETbinsFullRange;
  std::vector<float> m_ETbinsFullRange;

  //For the scale factors of the standard egamma cuts 
  //Release 15
  //Probes between 30 and 50 GeV (plateau region)
  std::vector<float> efficienciesRel15Loose3050;
  std::vector<float> uncertaintiesRel15Loose3050;
  std::vector<float> efficienciesRel15Medium3050;
  std::vector<float> uncertaintiesRel15Medium3050;
  std::vector<float> efficienciesRel15Tight3050;
  std::vector<float> uncertaintiesRel15Tight3050;
  //Probes between 20 and 50 GeV
  std::vector<float> efficienciesRel15Loose2050;
  std::vector<float> uncertaintiesRel15Loose2050;
  std::vector<float> efficienciesRel15Medium2050;
  std::vector<float> uncertaintiesRel15Medium2050;
  std::vector<float> efficienciesRel15Tight2050;
  std::vector<float> uncertaintiesRel15Tight2050;

  //Release 16
  //Probes between 30 and 50 GeV (plateau region)
  std::vector<float> efficienciesRel16Medium3050;
  std::vector<float> uncertaintiesRel16Medium3050;
  std::vector<float> efficienciesRel16Tight3050;
  std::vector<float> uncertaintiesRel16Tight3050;
  //Probes between 20 and 50 GeV
  std::vector<float> efficienciesRel16Medium2050;
  std::vector<float> uncertaintiesRel16Medium2050;
  std::vector<float> efficienciesRel16Tight2050;
  std::vector<float> uncertaintiesRel16Tight2050;

  //Release 16.6 with 2010 data
  //Probes between 30 and 50 GeV (plateau region)
  std::vector<float> efficienciesRel166Data2010Medium3050;
  std::vector<float> uncertaintiesRel166Data2010Medium3050;
  std::vector<float> efficienciesRel166Data2010Tight3050;
  std::vector<float> uncertaintiesRel166Data2010Tight3050;
  //Probes between 20 and 50 GeV
  std::vector<float> efficienciesRel166Data2010Medium2050;
  std::vector<float> uncertaintiesRel166Data2010Medium2050;
  std::vector<float> efficienciesRel166Data2010Tight2050;
  std::vector<float> uncertaintiesRel166Data2010Tight2050;

  //Release 16.6, EPS recommendations
  //Identification for probes between 20 and 50 GeV
  std::vector<float> efficienciesRel166EPSMedium2050;
  std::vector<float> uncertaintiesRel166EPSMedium2050;
  std::vector<float> efficienciesRel166EPSTight2050;
  std::vector<float> uncertaintiesRel166EPSTight2050;
  //Identification for low ET probes
  std::vector<float> efficienciesRel166EPSMediumLowET;
  std::vector<float> uncertaintiesRel166EPSMediumLowET;
  std::vector<float> efficienciesRel166EPSTightLowET;
  std::vector<float> uncertaintiesRel166EPSTightLowET;
  //For trigger efficiencies on the plateau
  std::vector<float> efficienciesRel166EPSTrigger;
  std::vector<float> uncertaintiesRel166EPSTrigger;
  //For reco+trkquality efficiencies
  std::vector<float> efficienciesRel166EPSRecoTrkQual;
  std::vector<float> uncertaintiesRel166EPSRecoTrkQual;

  //For the ET-corrections of the scale factors
  //Release 16
  //Medium
  std::vector<float> ETCorrectionsMediumRel16;
  std::vector<float> uncertaintiesETCorrectionsMediumRel16;
  //Tight
  std::vector<float> ETCorrectionsTightRel16;
  std::vector<float> uncertaintiesETCorrectionsTightRel16;
  //Release 16.6 with 2010 data
  //Medium
  std::vector<float> ETCorrectionsMediumRel166Data2010;
  std::vector<float> uncertaintiesETCorrectionsMediumRel166Data2010;
  //Tight
  std::vector<float> ETCorrectionsTightRel166Data2010;
  std::vector<float> uncertaintiesETCorrectionsTightRel166Data2010;
  //Release 16.6, EPS recommendations
  //Medium
  std::vector<float> ETCorrectionsMediumRel166EPS;
  std::vector<float> uncertaintiesETCorrectionsMediumRel166EPS;
  //Tight
  std::vector<float> ETCorrectionsTightRel166EPS;
  std::vector<float> uncertaintiesETCorrectionsTightRel166EPS;
  //Release 16.6, EPS recommendations including low ET electrons
  //Medium
  std::vector<float> ETCorrectionsMediumRel166EPSFullRange;
  std::vector<float> uncertaintiesETCorrectionsMediumRel166EPSFullRange;
  //Tight
  std::vector<float> ETCorrectionsTightRel166EPSFullRange;
  std::vector<float> uncertaintiesETCorrectionsTightRel166EPSFullRange;


};

#endif


