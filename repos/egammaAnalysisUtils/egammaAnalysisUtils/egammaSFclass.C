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

#include "egammaAnalysisUtils/egammaSFclass.h"
#include <cmath>

egammaSFclass::egammaSFclass()
{
  //Definition of the eta binning
  m_nEtabins=10;
  m_Etabins.push_back(-2.47);
  m_Etabins.push_back(-2.01); 
  m_Etabins.push_back(-1.52); 
  m_Etabins.push_back(-1.37); 
  m_Etabins.push_back(-0.8); 
  m_Etabins.push_back(0); 
  m_Etabins.push_back(0.8); 
  m_Etabins.push_back(1.37); 
  m_Etabins.push_back(1.52); 
  m_Etabins.push_back(2.01); 
  m_Etabins.push_back(2.47);
  //Definition of the fine eta binning
  m_nFineEtabins=20;
  m_FineEtabins.push_back(-2.47);
  m_FineEtabins.push_back(-2.37);
  m_FineEtabins.push_back(-2.01);
  m_FineEtabins.push_back(-1.81);
  m_FineEtabins.push_back(-1.52);
  m_FineEtabins.push_back(-1.37);
  m_FineEtabins.push_back(-1.15);
  m_FineEtabins.push_back(-0.8 );
  m_FineEtabins.push_back(-0.6 );
  m_FineEtabins.push_back(-0.1 );
  m_FineEtabins.push_back( 0.  );
  m_FineEtabins.push_back( 0.1 );
  m_FineEtabins.push_back( 0.6 );
  m_FineEtabins.push_back( 0.8 );
  m_FineEtabins.push_back( 1.15);
  m_FineEtabins.push_back( 1.37);
  m_FineEtabins.push_back( 1.52);
  m_FineEtabins.push_back( 1.81);
  m_FineEtabins.push_back( 2.01);
  m_FineEtabins.push_back( 2.37);
  m_FineEtabins.push_back( 2.47);
  //Definition of the ET binning
  m_nETbins=10;
  m_ETbins.push_back(0.);
  m_ETbins.push_back(20000.); 
  m_ETbins.push_back(25000.); 
  m_ETbins.push_back(30000.); 
  m_ETbins.push_back(35000.); 
  m_ETbins.push_back(40000.); 
  m_ETbins.push_back(45000.); 
  m_ETbins.push_back(500000000.); 
  //Definition of the ET binning on the full range
  m_nETbinsFullRange=12;
  m_ETbinsFullRange.push_back(    0.);
  m_ETbinsFullRange.push_back( 7000.);
  m_ETbinsFullRange.push_back(10000.);
  m_ETbinsFullRange.push_back(15000.);
  m_ETbinsFullRange.push_back(20000.); 
  m_ETbinsFullRange.push_back(25000.); 
  m_ETbinsFullRange.push_back(30000.); 
  m_ETbinsFullRange.push_back(35000.); 
  m_ETbinsFullRange.push_back(40000.); 
  m_ETbinsFullRange.push_back(45000.); 
  m_ETbinsFullRange.push_back(500000000.); 


  //For the scale factors of the standard egamma cuts 

  //Release 15
  //Probes between 30 and 50 GeV (plateau region)
  //Loose
  efficienciesRel15Loose3050.push_back(98.1); 
  efficienciesRel15Loose3050.push_back(99.0); 
  efficienciesRel15Loose3050.push_back(0.); 
  efficienciesRel15Loose3050.push_back(98.6); 
  efficienciesRel15Loose3050.push_back(99.5); 
  efficienciesRel15Loose3050.push_back(99.1); 
  efficienciesRel15Loose3050.push_back(98.8); 
  efficienciesRel15Loose3050.push_back(0.); 
  efficienciesRel15Loose3050.push_back(99.9); 
  efficienciesRel15Loose3050.push_back(98.2);
  uncertaintiesRel15Loose3050.push_back(1.6); 
  uncertaintiesRel15Loose3050.push_back( 1.5); 
  uncertaintiesRel15Loose3050.push_back(0.); 
  uncertaintiesRel15Loose3050.push_back( 1.5); 
  uncertaintiesRel15Loose3050.push_back( 1.5); 
  uncertaintiesRel15Loose3050.push_back( 1.5); 
  uncertaintiesRel15Loose3050.push_back( 1.5); 
  uncertaintiesRel15Loose3050.push_back(0.); 
  uncertaintiesRel15Loose3050.push_back( 1.5); 
  uncertaintiesRel15Loose3050.push_back( 1.6);
  //Medium
  efficienciesRel15Medium3050.push_back(95.4); 
  efficienciesRel15Medium3050.push_back(98.7);
  efficienciesRel15Medium3050.push_back(0.); 
  efficienciesRel15Medium3050.push_back(97.9);
  efficienciesRel15Medium3050.push_back(98.1);
  efficienciesRel15Medium3050.push_back(97.7); 
  efficienciesRel15Medium3050.push_back(97.9); 
  efficienciesRel15Medium3050.push_back(0.); 
  efficienciesRel15Medium3050.push_back(99.9); 
  efficienciesRel15Medium3050.push_back(97.4);
  uncertaintiesRel15Medium3050.push_back(1.7);
  uncertaintiesRel15Medium3050.push_back( 1.6);
  uncertaintiesRel15Medium3050.push_back(0.); 
  uncertaintiesRel15Medium3050.push_back( 1.6);
  uncertaintiesRel15Medium3050.push_back( 1.5); 
  uncertaintiesRel15Medium3050.push_back( 1.5); 
  uncertaintiesRel15Medium3050.push_back( 1.5); 
  uncertaintiesRel15Medium3050.push_back(0.); 
  uncertaintiesRel15Medium3050.push_back( 1.6);
  uncertaintiesRel15Medium3050.push_back( 1.7);
  //Tight
  efficienciesRel15Tight3050.push_back(92.3); 
  efficienciesRel15Tight3050.push_back(99.2); 
  efficienciesRel15Tight3050.push_back(0.);
  efficienciesRel15Tight3050.push_back(101.5); 
  efficienciesRel15Tight3050.push_back(98.9); 
  efficienciesRel15Tight3050.push_back(99.9);
  efficienciesRel15Tight3050.push_back(104.2); 
  efficienciesRel15Tight3050.push_back(0.);
  efficienciesRel15Tight3050.push_back(102.6); 
  efficienciesRel15Tight3050.push_back(95.5);
  uncertaintiesRel15Tight3050.push_back(3.3);
  uncertaintiesRel15Tight3050.push_back( 2.3); 
  uncertaintiesRel15Tight3050.push_back(0.);
  uncertaintiesRel15Tight3050.push_back( 2.0); 
  uncertaintiesRel15Tight3050.push_back( 1.8); 
  uncertaintiesRel15Tight3050.push_back( 1.8);
  uncertaintiesRel15Tight3050.push_back( 2.5); 
  uncertaintiesRel15Tight3050.push_back(0.); 
  uncertaintiesRel15Tight3050.push_back( 5.0); 
  uncertaintiesRel15Tight3050.push_back( 3.2);

  //Probes between 20 and 50 GeV
  //Loose
  efficienciesRel15Loose2050.push_back(97.6); 
  efficienciesRel15Loose2050.push_back(99.0); 
  efficienciesRel15Loose2050.push_back(0.); 
  efficienciesRel15Loose2050.push_back(98.2); 
  efficienciesRel15Loose2050.push_back(99.1); 
  efficienciesRel15Loose2050.push_back(98.8); 
  efficienciesRel15Loose2050.push_back(98.2); 
  efficienciesRel15Loose2050.push_back(0.); 
  efficienciesRel15Loose2050.push_back(99.6); 
  efficienciesRel15Loose2050.push_back(97.4);
  uncertaintiesRel15Loose2050.push_back(1.6); 
  uncertaintiesRel15Loose2050.push_back(1.5); 
  uncertaintiesRel15Loose2050.push_back(0.); 
  uncertaintiesRel15Loose2050.push_back( 1.5); 
  uncertaintiesRel15Loose2050.push_back( 1.5); 
  uncertaintiesRel15Loose2050.push_back( 1.5); 
  uncertaintiesRel15Loose2050.push_back( 1.5); 
  uncertaintiesRel15Loose2050.push_back(0.); 
  uncertaintiesRel15Loose2050.push_back( 1.5); 
  uncertaintiesRel15Loose2050.push_back( 1.6);
  //Medium
  efficienciesRel15Medium2050.push_back(94.5); 
  efficienciesRel15Medium2050.push_back(98.8);
  efficienciesRel15Medium2050.push_back(0.); 
  efficienciesRel15Medium2050.push_back(97.2);
  efficienciesRel15Medium2050.push_back(97.4);
  efficienciesRel15Medium2050.push_back(97.2); 
  efficienciesRel15Medium2050.push_back(96.7); 
  efficienciesRel15Medium2050.push_back(0.); 
  efficienciesRel15Medium2050.push_back(99.5); 
  efficienciesRel15Medium2050.push_back(96.1);
  uncertaintiesRel15Medium2050.push_back(1.7);
  uncertaintiesRel15Medium2050.push_back( 1.6);
  uncertaintiesRel15Medium2050.push_back(0.); 
  uncertaintiesRel15Medium2050.push_back( 1.6);
  uncertaintiesRel15Medium2050.push_back( 1.5); 
  uncertaintiesRel15Medium2050.push_back( 1.5); 
  uncertaintiesRel15Medium2050.push_back( 1.5); 
  uncertaintiesRel15Medium2050.push_back(0.); 
  uncertaintiesRel15Medium2050.push_back( 2.9);
  uncertaintiesRel15Medium2050.push_back( 1.7);
  //Tight
  efficienciesRel15Tight2050.push_back(92.5); 
  efficienciesRel15Tight2050.push_back(99.5); 
  efficienciesRel15Tight2050.push_back(0.);
  efficienciesRel15Tight2050.push_back(100.6); 
  efficienciesRel15Tight2050.push_back(98.2); 
  efficienciesRel15Tight2050.push_back(98.7);
  efficienciesRel15Tight2050.push_back(103.3); 
  efficienciesRel15Tight2050.push_back(0.);
  efficienciesRel15Tight2050.push_back(102.8); 
  efficienciesRel15Tight2050.push_back(93.6);
  uncertaintiesRel15Tight2050.push_back(3.4);
  uncertaintiesRel15Tight2050.push_back( 2.4); 
  uncertaintiesRel15Tight2050.push_back(0.);
  uncertaintiesRel15Tight2050.push_back( 2.1); 
  uncertaintiesRel15Tight2050.push_back( 1.8); 
  uncertaintiesRel15Tight2050.push_back( 1.8);
  uncertaintiesRel15Tight2050.push_back( 2.5); 
  uncertaintiesRel15Tight2050.push_back(0.); 
  uncertaintiesRel15Tight2050.push_back( 4.5); 
  uncertaintiesRel15Tight2050.push_back( 3.4);


  //Release 16
  //Probes between 30 and 50 GeV (plateau region)
  //Medium
  efficienciesRel16Medium3050.push_back(98.8); 
  efficienciesRel16Medium3050.push_back(98.0);
  efficienciesRel16Medium3050.push_back(96.9); 
  efficienciesRel16Medium3050.push_back(98.0);
  efficienciesRel16Medium3050.push_back(97.4);
  efficienciesRel16Medium3050.push_back(98.1); 
  efficienciesRel16Medium3050.push_back(98.1); 
  efficienciesRel16Medium3050.push_back(98.3); 
  efficienciesRel16Medium3050.push_back(98.6); 
  efficienciesRel16Medium3050.push_back(97.5);
  uncertaintiesRel16Medium3050.push_back(0.8);
  uncertaintiesRel16Medium3050.push_back(0.9);
  uncertaintiesRel16Medium3050.push_back(2.5); 
  uncertaintiesRel16Medium3050.push_back(0.8);
  uncertaintiesRel16Medium3050.push_back(0.7); 
  uncertaintiesRel16Medium3050.push_back(0.7); 
  uncertaintiesRel16Medium3050.push_back(0.8); 
  uncertaintiesRel16Medium3050.push_back(2.6); 
  uncertaintiesRel16Medium3050.push_back(0.8);
  uncertaintiesRel16Medium3050.push_back(0.8);
  //Tight
  efficienciesRel16Tight3050.push_back(102.0); 
  efficienciesRel16Tight3050.push_back(102.7); 
  efficienciesRel16Tight3050.push_back(114.4);
  efficienciesRel16Tight3050.push_back(106.7); 
  efficienciesRel16Tight3050.push_back( 99.0); 
  efficienciesRel16Tight3050.push_back(100.1);
  efficienciesRel16Tight3050.push_back(105.7); 
  efficienciesRel16Tight3050.push_back(110.8);
  efficienciesRel16Tight3050.push_back(104.2); 
  efficienciesRel16Tight3050.push_back(102.7);
  uncertaintiesRel16Tight3050.push_back(3.0);
  uncertaintiesRel16Tight3050.push_back(1.1); 
  uncertaintiesRel16Tight3050.push_back(3.9);
  uncertaintiesRel16Tight3050.push_back(1.1); 
  uncertaintiesRel16Tight3050.push_back(0.8); 
  uncertaintiesRel16Tight3050.push_back(0.8);
  uncertaintiesRel16Tight3050.push_back(0.9); 
  uncertaintiesRel16Tight3050.push_back(4.6); 
  uncertaintiesRel16Tight3050.push_back(2.6); 
  uncertaintiesRel16Tight3050.push_back(1.2);

  //Probes between 20 and 50 GeV
  //Medium
  efficienciesRel16Medium2050.push_back(97.6); 
  efficienciesRel16Medium2050.push_back(96.8);
  efficienciesRel16Medium2050.push_back(97.7); 
  efficienciesRel16Medium2050.push_back(97.1);
  efficienciesRel16Medium2050.push_back(96.8);
  efficienciesRel16Medium2050.push_back(97.6); 
  efficienciesRel16Medium2050.push_back(97.2); 
  efficienciesRel16Medium2050.push_back(98.2); 
  efficienciesRel16Medium2050.push_back(97.9); 
  efficienciesRel16Medium2050.push_back(96.2);
  uncertaintiesRel16Medium2050.push_back(1.0);
  uncertaintiesRel16Medium2050.push_back(1.0);
  uncertaintiesRel16Medium2050.push_back(3.3); 
  uncertaintiesRel16Medium2050.push_back(1.1);
  uncertaintiesRel16Medium2050.push_back(0.8); 
  uncertaintiesRel16Medium2050.push_back(0.8); 
  uncertaintiesRel16Medium2050.push_back(0.9); 
  uncertaintiesRel16Medium2050.push_back(3.2); 
  uncertaintiesRel16Medium2050.push_back(1.0);
  uncertaintiesRel16Medium2050.push_back(2.8);
  //Tight
  efficienciesRel16Tight2050.push_back(100.2); 
  efficienciesRel16Tight2050.push_back(101.5); 
  efficienciesRel16Tight2050.push_back(117.9);
  efficienciesRel16Tight2050.push_back(105.7); 
  efficienciesRel16Tight2050.push_back( 98.1); 
  efficienciesRel16Tight2050.push_back( 99.1);
  efficienciesRel16Tight2050.push_back(105.2); 
  efficienciesRel16Tight2050.push_back(113.9);
  efficienciesRel16Tight2050.push_back(103.8); 
  efficienciesRel16Tight2050.push_back(101.2);
  uncertaintiesRel16Tight2050.push_back(1.1);
  uncertaintiesRel16Tight2050.push_back(1.2); 
  uncertaintiesRel16Tight2050.push_back(4.4);
  uncertaintiesRel16Tight2050.push_back(1.5); 
  uncertaintiesRel16Tight2050.push_back(0.9); 
  uncertaintiesRel16Tight2050.push_back(1.0);
  uncertaintiesRel16Tight2050.push_back(1.1); 
  uncertaintiesRel16Tight2050.push_back(5.2); 
  uncertaintiesRel16Tight2050.push_back(3.0); 
  uncertaintiesRel16Tight2050.push_back(1.3);


  //For the ET-corrections of the scale factors
  //Medium
  ETCorrectionsMediumRel16.push_back( 79.6);
  ETCorrectionsMediumRel16.push_back( 93.9);
  ETCorrectionsMediumRel16.push_back( 96.2);
  ETCorrectionsMediumRel16.push_back( 99.7);
  ETCorrectionsMediumRel16.push_back(100.6);
  ETCorrectionsMediumRel16.push_back(100.4);
  ETCorrectionsMediumRel16.push_back(101.00);
  uncertaintiesETCorrectionsMediumRel16.push_back( 9.4);
  uncertaintiesETCorrectionsMediumRel16.push_back( 3.6);
  uncertaintiesETCorrectionsMediumRel16.push_back( 1.4);
  uncertaintiesETCorrectionsMediumRel16.push_back( 0.7);
  uncertaintiesETCorrectionsMediumRel16.push_back( 0.5);
  uncertaintiesETCorrectionsMediumRel16.push_back( 0.7);
  uncertaintiesETCorrectionsMediumRel16.push_back( 1.7);
  //Medium
  ETCorrectionsTightRel16.push_back( 76.7);
  ETCorrectionsTightRel16.push_back( 93.6);
  ETCorrectionsTightRel16.push_back( 95.1);
  ETCorrectionsTightRel16.push_back( 99.9);
  ETCorrectionsTightRel16.push_back(100.4);
  ETCorrectionsTightRel16.push_back(100.0);
  ETCorrectionsTightRel16.push_back(100.7);
  uncertaintiesETCorrectionsTightRel16.push_back(10.0);
  uncertaintiesETCorrectionsTightRel16.push_back( 3.7);
  uncertaintiesETCorrectionsTightRel16.push_back( 1.6);
  uncertaintiesETCorrectionsTightRel16.push_back( 0.9);
  uncertaintiesETCorrectionsTightRel16.push_back( 0.7);
  uncertaintiesETCorrectionsTightRel16.push_back( 0.9);
  uncertaintiesETCorrectionsTightRel16.push_back( 1.8);



  //Release 16.6 Data 2010
  //Probes between 30 and 50 GeV (plateau region)
  //Medium
  efficienciesRel166Data2010Medium3050.push_back(98.44); 
  efficienciesRel166Data2010Medium3050.push_back(96.93);
  efficienciesRel166Data2010Medium3050.push_back(96.61); 
  efficienciesRel166Data2010Medium3050.push_back(96.87);
  efficienciesRel166Data2010Medium3050.push_back(97.06);
  efficienciesRel166Data2010Medium3050.push_back(97.49); 
  efficienciesRel166Data2010Medium3050.push_back(97.04); 
  efficienciesRel166Data2010Medium3050.push_back(97.17); 
  efficienciesRel166Data2010Medium3050.push_back(97.31); 
  efficienciesRel166Data2010Medium3050.push_back(97.51);
  uncertaintiesRel166Data2010Medium3050.push_back(2.14);
  uncertaintiesRel166Data2010Medium3050.push_back(2.20);
  uncertaintiesRel166Data2010Medium3050.push_back(2.84); 
  uncertaintiesRel166Data2010Medium3050.push_back(2.13);
  uncertaintiesRel166Data2010Medium3050.push_back(2.18); 
  uncertaintiesRel166Data2010Medium3050.push_back(2.10); 
  uncertaintiesRel166Data2010Medium3050.push_back(2.13); 
  uncertaintiesRel166Data2010Medium3050.push_back(2.89); 
  uncertaintiesRel166Data2010Medium3050.push_back(2.13);
  uncertaintiesRel166Data2010Medium3050.push_back(2.21);
  //Tight
  efficienciesRel166Data2010Tight3050.push_back(101.47); 
  efficienciesRel166Data2010Tight3050.push_back(104.02); 
  efficienciesRel166Data2010Tight3050.push_back(112.70);
  efficienciesRel166Data2010Tight3050.push_back(106.82); 
  efficienciesRel166Data2010Tight3050.push_back( 99.35); 
  efficienciesRel166Data2010Tight3050.push_back(100.13);
  efficienciesRel166Data2010Tight3050.push_back(105.94); 
  efficienciesRel166Data2010Tight3050.push_back(113.57);
  efficienciesRel166Data2010Tight3050.push_back(105.48); 
  efficienciesRel166Data2010Tight3050.push_back(101.99);
  uncertaintiesRel166Data2010Tight3050.push_back(3.46);
  uncertaintiesRel166Data2010Tight3050.push_back(2.65); 
  uncertaintiesRel166Data2010Tight3050.push_back(3.65);
  uncertaintiesRel166Data2010Tight3050.push_back(2.49); 
  uncertaintiesRel166Data2010Tight3050.push_back(2.33); 
  uncertaintiesRel166Data2010Tight3050.push_back(2.28);
  uncertaintiesRel166Data2010Tight3050.push_back(2.45); 
  uncertaintiesRel166Data2010Tight3050.push_back(3.72); 
  uncertaintiesRel166Data2010Tight3050.push_back(3.38); 
  uncertaintiesRel166Data2010Tight3050.push_back(2.70);

  //Probes between 20 and 50 GeV
  //Medium
  efficienciesRel166Data2010Medium2050.push_back(97.35); 
  efficienciesRel166Data2010Medium2050.push_back(95.86);
  efficienciesRel166Data2010Medium2050.push_back(96.25); 
  efficienciesRel166Data2010Medium2050.push_back(95.80);
  efficienciesRel166Data2010Medium2050.push_back(96.01);
  efficienciesRel166Data2010Medium2050.push_back(96.84); 
  efficienciesRel166Data2010Medium2050.push_back(96.04); 
  efficienciesRel166Data2010Medium2050.push_back(96.54); 
  efficienciesRel166Data2010Medium2050.push_back(96.59); 
  efficienciesRel166Data2010Medium2050.push_back(96.33);
  uncertaintiesRel166Data2010Medium2050.push_back(2.21);
  uncertaintiesRel166Data2010Medium2050.push_back(2.25);
  uncertaintiesRel166Data2010Medium2050.push_back(3.22); 
  uncertaintiesRel166Data2010Medium2050.push_back(2.27);
  uncertaintiesRel166Data2010Medium2050.push_back(2.23); 
  uncertaintiesRel166Data2010Medium2050.push_back(2.13); 
  uncertaintiesRel166Data2010Medium2050.push_back(2.17); 
  uncertaintiesRel166Data2010Medium2050.push_back(3.20); 
  uncertaintiesRel166Data2010Medium2050.push_back(2.24);
  uncertaintiesRel166Data2010Medium2050.push_back(2.41);
  //Tight
  efficienciesRel166Data2010Tight2050.push_back(99.90); 
  efficienciesRel166Data2010Tight2050.push_back(103.11); 
  efficienciesRel166Data2010Tight2050.push_back(116.16);
  efficienciesRel166Data2010Tight2050.push_back(105.70); 
  efficienciesRel166Data2010Tight2050.push_back( 97.98); 
  efficienciesRel166Data2010Tight2050.push_back( 99.08);
  efficienciesRel166Data2010Tight2050.push_back(105.23); 
  efficienciesRel166Data2010Tight2050.push_back(115.12);
  efficienciesRel166Data2010Tight2050.push_back(104.91); 
  efficienciesRel166Data2010Tight2050.push_back(101.99);
  uncertaintiesRel166Data2010Tight2050.push_back(2.28);
  uncertaintiesRel166Data2010Tight2050.push_back(2.89); 
  uncertaintiesRel166Data2010Tight2050.push_back(4.35);
  uncertaintiesRel166Data2010Tight2050.push_back(2.72); 
  uncertaintiesRel166Data2010Tight2050.push_back(2.40); 
  uncertaintiesRel166Data2010Tight2050.push_back(2.24);
  uncertaintiesRel166Data2010Tight2050.push_back(2.48); 
  uncertaintiesRel166Data2010Tight2050.push_back(4.17); 
  uncertaintiesRel166Data2010Tight2050.push_back(2.45); 
  uncertaintiesRel166Data2010Tight2050.push_back(3.29);
  //For the ET-corrections of the scale factors
  //Medium
  ETCorrectionsMediumRel166Data2010.push_back(80.60);
  ETCorrectionsMediumRel166Data2010.push_back(92.07);
  ETCorrectionsMediumRel166Data2010.push_back(96.34);
  ETCorrectionsMediumRel166Data2010.push_back(100.19);
  ETCorrectionsMediumRel166Data2010.push_back(101.54);
  ETCorrectionsMediumRel166Data2010.push_back(101.25);
  ETCorrectionsMediumRel166Data2010.push_back(102.29);
  uncertaintiesETCorrectionsMediumRel166Data2010.push_back( 9.60);
  uncertaintiesETCorrectionsMediumRel166Data2010.push_back( 3.27);
  uncertaintiesETCorrectionsMediumRel166Data2010.push_back( 1.40);
  uncertaintiesETCorrectionsMediumRel166Data2010.push_back( 0.70);
  uncertaintiesETCorrectionsMediumRel166Data2010.push_back( 0.53);
  uncertaintiesETCorrectionsMediumRel166Data2010.push_back( 0.74);
  uncertaintiesETCorrectionsMediumRel166Data2010.push_back( 1.59);
  //Tight
  ETCorrectionsTightRel166Data2010.push_back(77.78);
  ETCorrectionsTightRel166Data2010.push_back(91.84);
  ETCorrectionsTightRel166Data2010.push_back(95.67);
  ETCorrectionsTightRel166Data2010.push_back(100.86);
  ETCorrectionsTightRel166Data2010.push_back(101.83);
  ETCorrectionsTightRel166Data2010.push_back(101.33);
  ETCorrectionsTightRel166Data2010.push_back(102.10);
  uncertaintiesETCorrectionsTightRel166Data2010.push_back(10.29);
  uncertaintiesETCorrectionsTightRel166Data2010.push_back( 3.47);
  uncertaintiesETCorrectionsTightRel166Data2010.push_back( 1.52);
  uncertaintiesETCorrectionsTightRel166Data2010.push_back( 1.04);
  uncertaintiesETCorrectionsTightRel166Data2010.push_back( 0.66);
  uncertaintiesETCorrectionsTightRel166Data2010.push_back( 0.92);
  uncertaintiesETCorrectionsTightRel166Data2010.push_back( 1.90);


  //Release 16.6 Data 2011 EPS recommendations
  //Identification for probes between 20 and 50 GeV
  //Medium
  efficienciesRel166EPSMedium2050.push_back(95.7273);
  efficienciesRel166EPSMedium2050.push_back(95.5243);
  efficienciesRel166EPSMedium2050.push_back(96.403);
  efficienciesRel166EPSMedium2050.push_back(96.3494);
  efficienciesRel166EPSMedium2050.push_back(97.9518);
  efficienciesRel166EPSMedium2050.push_back(96.3292);
  efficienciesRel166EPSMedium2050.push_back(97.0952);
  efficienciesRel166EPSMedium2050.push_back(96.3317);
  efficienciesRel166EPSMedium2050.push_back(97.1977);
  efficienciesRel166EPSMedium2050.push_back(97.8678);
  efficienciesRel166EPSMedium2050.push_back(96.5697);
  efficienciesRel166EPSMedium2050.push_back(96.7783);
  efficienciesRel166EPSMedium2050.push_back(97.0532);
  efficienciesRel166EPSMedium2050.push_back(96.4621);
  efficienciesRel166EPSMedium2050.push_back(95.3501);
  efficienciesRel166EPSMedium2050.push_back(97.9656);
  efficienciesRel166EPSMedium2050.push_back(96.3031);
  efficienciesRel166EPSMedium2050.push_back(97.3978);
  efficienciesRel166EPSMedium2050.push_back(95.7546);
  efficienciesRel166EPSMedium2050.push_back(97.2443);
  uncertaintiesRel166EPSMedium2050.push_back(0.758538);
  uncertaintiesRel166EPSMedium2050.push_back(1.48083);
  uncertaintiesRel166EPSMedium2050.push_back(0.778086);
  uncertaintiesRel166EPSMedium2050.push_back(0.496963);
  uncertaintiesRel166EPSMedium2050.push_back(1.0011);
  uncertaintiesRel166EPSMedium2050.push_back(0.694056);
  uncertaintiesRel166EPSMedium2050.push_back(0.603261);
  uncertaintiesRel166EPSMedium2050.push_back(0.719089);
  uncertaintiesRel166EPSMedium2050.push_back(0.635625);
  uncertaintiesRel166EPSMedium2050.push_back(0.825545);
  uncertaintiesRel166EPSMedium2050.push_back(0.777055);
  uncertaintiesRel166EPSMedium2050.push_back(0.655198);
  uncertaintiesRel166EPSMedium2050.push_back(0.736623);
  uncertaintiesRel166EPSMedium2050.push_back(0.633197);
  uncertaintiesRel166EPSMedium2050.push_back(1.04172);
  uncertaintiesRel166EPSMedium2050.push_back(0.612204);
  uncertaintiesRel166EPSMedium2050.push_back(0.47725);
  uncertaintiesRel166EPSMedium2050.push_back(1.32532);
  uncertaintiesRel166EPSMedium2050.push_back(0.74313);
  uncertaintiesRel166EPSMedium2050.push_back(1.44683);
  //Tight
  efficienciesRel166EPSTight2050.push_back( 99.9569);
  efficienciesRel166EPSTight2050.push_back( 99.1664);
  efficienciesRel166EPSTight2050.push_back(103.421 );
  efficienciesRel166EPSTight2050.push_back(102.688 );
  efficienciesRel166EPSTight2050.push_back(113.028 );
  efficienciesRel166EPSTight2050.push_back(111.078 );
  efficienciesRel166EPSTight2050.push_back(103.481 );
  efficienciesRel166EPSTight2050.push_back( 99.5783);
  efficienciesRel166EPSTight2050.push_back( 98.4303);
  efficienciesRel166EPSTight2050.push_back(100.837 );
  efficienciesRel166EPSTight2050.push_back( 99.1868);
  efficienciesRel166EPSTight2050.push_back( 98.1188);
  efficienciesRel166EPSTight2050.push_back(100.492 );
  efficienciesRel166EPSTight2050.push_back(102.816 );
  efficienciesRel166EPSTight2050.push_back(109.09  );
  efficienciesRel166EPSTight2050.push_back(113.772 );
  efficienciesRel166EPSTight2050.push_back(103.355 );
  efficienciesRel166EPSTight2050.push_back(103.454 );
  efficienciesRel166EPSTight2050.push_back( 98.4376);
  efficienciesRel166EPSTight2050.push_back(102.174 );
  uncertaintiesRel166EPSTight2050.push_back(2.82899);
  uncertaintiesRel166EPSTight2050.push_back(1.47076);
  uncertaintiesRel166EPSTight2050.push_back(2.64305);
  uncertaintiesRel166EPSTight2050.push_back(0.692373);
  uncertaintiesRel166EPSTight2050.push_back(2.0146 );
  uncertaintiesRel166EPSTight2050.push_back(0.967662);
  uncertaintiesRel166EPSTight2050.push_back(0.714802);
  uncertaintiesRel166EPSTight2050.push_back(0.807023);
  uncertaintiesRel166EPSTight2050.push_back(0.686988);
  uncertaintiesRel166EPSTight2050.push_back(1.4562);
  uncertaintiesRel166EPSTight2050.push_back(0.984975);
  uncertaintiesRel166EPSTight2050.push_back(0.703155);
  uncertaintiesRel166EPSTight2050.push_back(0.80346);
  uncertaintiesRel166EPSTight2050.push_back(0.742777);
  uncertaintiesRel166EPSTight2050.push_back(1.78409);
  uncertaintiesRel166EPSTight2050.push_back(1.13598);
  uncertaintiesRel166EPSTight2050.push_back(0.716145);
  uncertaintiesRel166EPSTight2050.push_back(2.28302);
  uncertaintiesRel166EPSTight2050.push_back(1.13891);
  uncertaintiesRel166EPSTight2050.push_back(2.02877);
  //Identification for low ET probes
  //Medium
  efficienciesRel166EPSMediumLowET.push_back(91.16);
  efficienciesRel166EPSMediumLowET.push_back(99.84);
  efficienciesRel166EPSMediumLowET.push_back( 0.00);
  efficienciesRel166EPSMediumLowET.push_back(101.4);
  efficienciesRel166EPSMediumLowET.push_back(96.76);
  efficienciesRel166EPSMediumLowET.push_back(98.11);
  efficienciesRel166EPSMediumLowET.push_back(96.75);
  efficienciesRel166EPSMediumLowET.push_back( 0.00);
  efficienciesRel166EPSMediumLowET.push_back(86.38);
  efficienciesRel166EPSMediumLowET.push_back(84.37);
  uncertaintiesRel166EPSMediumLowET.push_back(11.0);
  uncertaintiesRel166EPSMediumLowET.push_back( 8.5);
  uncertaintiesRel166EPSMediumLowET.push_back( 0.0);
  uncertaintiesRel166EPSMediumLowET.push_back(10.8);
  uncertaintiesRel166EPSMediumLowET.push_back( 6.7);
  uncertaintiesRel166EPSMediumLowET.push_back( 7.0);
  uncertaintiesRel166EPSMediumLowET.push_back( 7.2);
  uncertaintiesRel166EPSMediumLowET.push_back( 0.0);
  uncertaintiesRel166EPSMediumLowET.push_back(10.1);
  uncertaintiesRel166EPSMediumLowET.push_back(10.2);
  //Tight
  efficienciesRel166EPSTightLowET.push_back(91.67);
  efficienciesRel166EPSTightLowET.push_back(100.6);
  efficienciesRel166EPSTightLowET.push_back( 0.00);
  efficienciesRel166EPSTightLowET.push_back(101.1);
  efficienciesRel166EPSTightLowET.push_back(96.88);
  efficienciesRel166EPSTightLowET.push_back(98.14);
  efficienciesRel166EPSTightLowET.push_back(98.23);
  efficienciesRel166EPSTightLowET.push_back( 0.00);
  efficienciesRel166EPSTightLowET.push_back(86.59);
  efficienciesRel166EPSTightLowET.push_back(84.39);
  uncertaintiesRel166EPSTightLowET.push_back(10.9);
  uncertaintiesRel166EPSTightLowET.push_back( 9.6);
  uncertaintiesRel166EPSTightLowET.push_back( 0.0);
  uncertaintiesRel166EPSTightLowET.push_back(10.5);
  uncertaintiesRel166EPSTightLowET.push_back( 6.1);
  uncertaintiesRel166EPSTightLowET.push_back( 6.1);
  uncertaintiesRel166EPSTightLowET.push_back( 9.5);
  uncertaintiesRel166EPSTightLowET.push_back( 0.0);
  uncertaintiesRel166EPSTightLowET.push_back(11.3);
  uncertaintiesRel166EPSTightLowET.push_back( 8.6);
  //For the ET-corrections of the identification scale factors
  //Medium
  ETCorrectionsMediumRel166EPS.push_back( 87.0781);
  ETCorrectionsMediumRel166EPS.push_back( 90.9091);
  ETCorrectionsMediumRel166EPS.push_back( 97.3568);
  ETCorrectionsMediumRel166EPS.push_back(100.453);
  ETCorrectionsMediumRel166EPS.push_back(101.55);
  ETCorrectionsMediumRel166EPS.push_back(101.365);
  ETCorrectionsMediumRel166EPS.push_back(102.087);
  uncertaintiesETCorrectionsMediumRel166EPS.push_back(6.00538);
  uncertaintiesETCorrectionsMediumRel166EPS.push_back(2.62057);
  uncertaintiesETCorrectionsMediumRel166EPS.push_back(0.93479);
  uncertaintiesETCorrectionsMediumRel166EPS.push_back(0.94788);
  uncertaintiesETCorrectionsMediumRel166EPS.push_back(0.43064);
  uncertaintiesETCorrectionsMediumRel166EPS.push_back(0.40351);
  uncertaintiesETCorrectionsMediumRel166EPS.push_back(0.53891);
  //Tight
  ETCorrectionsTightRel166EPS.push_back( 84.3469);
  ETCorrectionsTightRel166EPS.push_back( 89.3899);
  ETCorrectionsTightRel166EPS.push_back( 97.1825);
  ETCorrectionsTightRel166EPS.push_back(100.33);
  ETCorrectionsTightRel166EPS.push_back(101.319);
  ETCorrectionsTightRel166EPS.push_back(101.238);
  ETCorrectionsTightRel166EPS.push_back(101.552);
  uncertaintiesETCorrectionsTightRel166EPS.push_back(6.52625);
  uncertaintiesETCorrectionsTightRel166EPS.push_back(2.75939);
  uncertaintiesETCorrectionsTightRel166EPS.push_back(1.6303);
  uncertaintiesETCorrectionsTightRel166EPS.push_back(1.29104);
  uncertaintiesETCorrectionsTightRel166EPS.push_back(0.420933);
  uncertaintiesETCorrectionsTightRel166EPS.push_back(0.435997);
  uncertaintiesETCorrectionsTightRel166EPS.push_back(1.05739);
  //For the low ET electrons
  //Medium
  ETCorrectionsMediumRel166EPSFullRange.push_back(0.000/0.9666);
  ETCorrectionsMediumRel166EPSFullRange.push_back(97.36/0.9666);
  ETCorrectionsMediumRel166EPSFullRange.push_back(93.55/0.9666);
  uncertaintiesETCorrectionsMediumRel166EPSFullRange.push_back(7.25/0.9666);
  uncertaintiesETCorrectionsMediumRel166EPSFullRange.push_back(7.41/0.9666);
  uncertaintiesETCorrectionsMediumRel166EPSFullRange.push_back(8.57/0.9666);
  ETCorrectionsMediumRel166EPSFullRange.push_back( 87.0781);
  ETCorrectionsMediumRel166EPSFullRange.push_back( 90.9091);
  ETCorrectionsMediumRel166EPSFullRange.push_back( 97.3568);
  ETCorrectionsMediumRel166EPSFullRange.push_back(100.453);
  ETCorrectionsMediumRel166EPSFullRange.push_back(101.55);
  ETCorrectionsMediumRel166EPSFullRange.push_back(101.365);
  ETCorrectionsMediumRel166EPSFullRange.push_back(102.087);
  uncertaintiesETCorrectionsMediumRel166EPSFullRange.push_back(9.18078);
  uncertaintiesETCorrectionsMediumRel166EPSFullRange.push_back(2.62057);
  uncertaintiesETCorrectionsMediumRel166EPSFullRange.push_back(0.93479);
  uncertaintiesETCorrectionsMediumRel166EPSFullRange.push_back(0.94788);
  uncertaintiesETCorrectionsMediumRel166EPSFullRange.push_back(0.43064);
  uncertaintiesETCorrectionsMediumRel166EPSFullRange.push_back(0.40351);
  uncertaintiesETCorrectionsMediumRel166EPSFullRange.push_back(0.53891);
  //Tight
  ETCorrectionsTightRel166EPSFullRange.push_back(0.000/0.9673);
  ETCorrectionsTightRel166EPSFullRange.push_back(105.8/0.9673);
  ETCorrectionsTightRel166EPSFullRange.push_back(98.8/0.9673);
  uncertaintiesETCorrectionsTightRel166EPSFullRange.push_back(10.24/0.9673);
  uncertaintiesETCorrectionsTightRel166EPSFullRange.push_back(10.43/0.9673);  
  uncertaintiesETCorrectionsTightRel166EPSFullRange.push_back(10.50/0.9673);
  ETCorrectionsTightRel166EPSFullRange.push_back( 84.3469);
  ETCorrectionsTightRel166EPSFullRange.push_back( 89.3899);
  ETCorrectionsTightRel166EPSFullRange.push_back( 97.1825);
  ETCorrectionsTightRel166EPSFullRange.push_back(100.33);
  ETCorrectionsTightRel166EPSFullRange.push_back(101.319);
  ETCorrectionsTightRel166EPSFullRange.push_back(101.238);
  ETCorrectionsTightRel166EPSFullRange.push_back(101.552);
  uncertaintiesETCorrectionsTightRel166EPSFullRange.push_back(10.1599);
  uncertaintiesETCorrectionsTightRel166EPSFullRange.push_back(2.75939);
  uncertaintiesETCorrectionsTightRel166EPSFullRange.push_back(1.6303);
  uncertaintiesETCorrectionsTightRel166EPSFullRange.push_back(1.29104);
  uncertaintiesETCorrectionsTightRel166EPSFullRange.push_back(0.420933);
  uncertaintiesETCorrectionsTightRel166EPSFullRange.push_back(0.435997);
  uncertaintiesETCorrectionsTightRel166EPSFullRange.push_back(1.05739);
  //Trigger efficiency scale factors
  efficienciesRel166EPSTrigger.push_back(96.5517);
  efficienciesRel166EPSTrigger.push_back(97.3861);
  efficienciesRel166EPSTrigger.push_back(98.4245);
  efficienciesRel166EPSTrigger.push_back(98.6712);
  efficienciesRel166EPSTrigger.push_back(97.7936);
  efficienciesRel166EPSTrigger.push_back(99.7033);
  efficienciesRel166EPSTrigger.push_back(98.9571);
  efficienciesRel166EPSTrigger.push_back(98.4703);
  efficienciesRel166EPSTrigger.push_back(99.3016);
  efficienciesRel166EPSTrigger.push_back(99.1186);
  efficienciesRel166EPSTrigger.push_back(99.2838);
  efficienciesRel166EPSTrigger.push_back(99.2266);
  efficienciesRel166EPSTrigger.push_back(99.709);
  efficienciesRel166EPSTrigger.push_back(99.1478);
  efficienciesRel166EPSTrigger.push_back(99.5733);
  efficienciesRel166EPSTrigger.push_back(98.9866);
  efficienciesRel166EPSTrigger.push_back(99.8198);
  efficienciesRel166EPSTrigger.push_back(97.821);
  efficienciesRel166EPSTrigger.push_back(97.862);
  efficienciesRel166EPSTrigger.push_back(97.901);
  uncertaintiesRel166EPSTrigger.push_back(0.645476);
  uncertaintiesRel166EPSTrigger.push_back(0.588429);
  uncertaintiesRel166EPSTrigger.push_back(0.432384);
  uncertaintiesRel166EPSTrigger.push_back(0.43052);
  uncertaintiesRel166EPSTrigger.push_back(0.579508);
  uncertaintiesRel166EPSTrigger.push_back(0.410817);
  uncertaintiesRel166EPSTrigger.push_back(0.457);
  uncertaintiesRel166EPSTrigger.push_back(0.515013);
  uncertaintiesRel166EPSTrigger.push_back(0.402588);
  uncertaintiesRel166EPSTrigger.push_back(0.418344);
  uncertaintiesRel166EPSTrigger.push_back(0.415669);
  uncertaintiesRel166EPSTrigger.push_back(0.404291);
  uncertaintiesRel166EPSTrigger.push_back(0.407594);
  uncertaintiesRel166EPSTrigger.push_back(0.460203);
  uncertaintiesRel166EPSTrigger.push_back(0.410275);
  uncertaintiesRel166EPSTrigger.push_back(0.53542);
  uncertaintiesRel166EPSTrigger.push_back(0.425722);
  uncertaintiesRel166EPSTrigger.push_back(0.667037);
  uncertaintiesRel166EPSTrigger.push_back(0.426163);
  uncertaintiesRel166EPSTrigger.push_back(0.976323);
  //Reco+trackquality efficiencies
  efficienciesRel166EPSRecoTrkQual.push_back( 97.59);
  efficienciesRel166EPSRecoTrkQual.push_back(100.91);
  efficienciesRel166EPSRecoTrkQual.push_back(100.91);
  efficienciesRel166EPSRecoTrkQual.push_back(100.91);
  efficienciesRel166EPSRecoTrkQual.push_back(100.91);
  efficienciesRel166EPSRecoTrkQual.push_back(100.91);
  efficienciesRel166EPSRecoTrkQual.push_back(100.91);
  efficienciesRel166EPSRecoTrkQual.push_back( 99.84);
  efficienciesRel166EPSRecoTrkQual.push_back( 99.84);
  efficienciesRel166EPSRecoTrkQual.push_back( 99.84);
  efficienciesRel166EPSRecoTrkQual.push_back( 99.84);
  efficienciesRel166EPSRecoTrkQual.push_back( 99.84);
  efficienciesRel166EPSRecoTrkQual.push_back( 99.84);
  efficienciesRel166EPSRecoTrkQual.push_back(100.91);
  efficienciesRel166EPSRecoTrkQual.push_back(100.91);
  efficienciesRel166EPSRecoTrkQual.push_back(100.91);
  efficienciesRel166EPSRecoTrkQual.push_back(100.91);
  efficienciesRel166EPSRecoTrkQual.push_back(100.91);
  efficienciesRel166EPSRecoTrkQual.push_back(100.91);
  efficienciesRel166EPSRecoTrkQual.push_back( 97.59);
  uncertaintiesRel166EPSRecoTrkQual.push_back(1.84);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.70);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.70);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.70);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.70);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.70);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.70);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.66);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.66);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.66);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.66);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.66);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.66);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.70);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.70);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.70);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.70);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.70);
  uncertaintiesRel166EPSRecoTrkQual.push_back(0.70);
  uncertaintiesRel166EPSRecoTrkQual.push_back(1.84);




}

std::pair<float,float> egammaSFclass::scaleFactor(float eta, float ET, int set, int range, int rel, bool etcorrection) {

   std::vector<float> * vectEff=0;
   std::vector<float> * vectUnc=0;
   std::vector<float> * vectEtaBinning=0;

   if (rel==4) { //release 16.6 numbers estimated from 2011 data, "EPS recommendations" including the low ET region
     vectEtaBinning = &m_FineEtabins;
     if (range==0) { //20-50 GeV region
       if (set==0 || set>4) {
	 std::cout << "egammaSFclass: ERROR : only Medium, Tight and trigger scale factors exist" << std::endl;
	 return make_pair(-1.,-1.);
       }
       else if (set==1) {//Medium
	 if (ET>15000.) {
	   vectEff = &efficienciesRel166EPSMedium2050;
	   vectUnc = &uncertaintiesRel166EPSMedium2050;
	 }
	 else {
	   vectEtaBinning = &m_Etabins;
	   vectEff = &efficienciesRel166EPSMediumLowET;
	   vectUnc = &uncertaintiesRel166EPSMediumLowET;
	 }
       }
       else if (set==2) {//Tight
	 if (ET>15000.) {
	   vectEff = &efficienciesRel166EPSTight2050;
	   vectUnc = &uncertaintiesRel166EPSTight2050;
	 }
	 else {
	   vectEtaBinning = &m_Etabins;
	   vectEff = &efficienciesRel166EPSTightLowET;
	   vectUnc = &uncertaintiesRel166EPSTightLowET;
	 }
       }
       else if (set==3) {//Trigger
	 vectEff = &efficienciesRel166EPSTrigger;
	 vectUnc = &uncertaintiesRel166EPSTrigger;
       }
       else if (set==4) {//Reco + track quality requirements
	 vectEff = &efficienciesRel166EPSRecoTrkQual;
	 vectUnc = &uncertaintiesRel166EPSRecoTrkQual;
	 if (ET<15000.) {
	   float eff=1.,unc=0.05;
	   if (fabs(eta)<1.37) {
	     eff=1.;unc=0.02;
	   }
	   return make_pair(eff,unc);
	 }
       }
     }//endif 20-50 GeV
     else {
	 std::cout << "egammaSFclass: ERROR : invalid range" << std::endl;
	 return make_pair(-1.,-1.);
     }
   } 
   else if (rel==3) { //release 16.6 numbers estimated from 2011 data, "EPS recommendations"
     vectEtaBinning = &m_FineEtabins;
     if (range==0) { //20-50 GeV region
       if (set==0 || set>4) {
	 std::cout << "egammaSFclass: ERROR : only Medium, Tight and trigger scale factors exist" << std::endl;
	 return make_pair(-1.,-1.);
       }
       else if (set==1) {//Medium
	 vectEff = &efficienciesRel166EPSMedium2050;
	 vectUnc = &uncertaintiesRel166EPSMedium2050;
       }
       else if (set==2) {//Tight
	 vectEff = &efficienciesRel166EPSTight2050;
	 vectUnc = &uncertaintiesRel166EPSTight2050;
       }
       else if (set==3) {//Trigger
	 vectEff = &efficienciesRel166EPSTrigger;
	 vectUnc = &uncertaintiesRel166EPSTrigger;
       }
       else if (set==4) {//Reco + track quality requirements
	 vectEff = &efficienciesRel166EPSRecoTrkQual;
	 vectUnc = &uncertaintiesRel166EPSRecoTrkQual;
       }
     }//endif 20-50 GeV
     else {
	 std::cout << "egammaSFclass: ERROR : invalid range" << std::endl;
	 return make_pair(-1.,-1.);
     }
   } 
   else if (rel==2) { //release 16.6 numbers estimated from 2010 data
     vectEtaBinning = &m_Etabins;
     if (range==0) { //20-50 GeV region
       if (set==0 || set>2) {//Loose
	 std::cout << "egammaSFclass: ERROR : only Medium and Tight scale factors exist" << std::endl;
	 return make_pair(-1.,-1.);
       }
       else if (set==1) {//Medium
	 vectEff = &efficienciesRel166Data2010Medium2050;
	 vectUnc = &uncertaintiesRel166Data2010Medium2050;
       }
       else if (set==2) {//Tight
	 vectEff = &efficienciesRel166Data2010Tight2050;
	 vectUnc = &uncertaintiesRel166Data2010Tight2050;
       }
     }//endif 20-50 GeV
     else if (range==1) { //30-50 GeV region
       if (set==0 || set>2) {//Loose
	 std::cout << "egammaSFclass: ERROR : only Medium and Tight scale factors exist" << std::endl;
	 return make_pair(-1.,-1.);
       }
       else if (set==1) {//Medium
	 vectEff = &efficienciesRel166Data2010Medium3050;
	 vectUnc = &uncertaintiesRel166Data2010Medium3050;
       }
       else if (set==2) {//Tight
	 vectEff = &efficienciesRel166Data2010Tight3050;
	 vectUnc = &uncertaintiesRel166Data2010Tight3050;
       }
     }//endif 30-50 GeV
     else {
	 std::cout << "egammaSFclass: ERROR : invalid range" << std::endl;
	 return make_pair(-1.,-1.);
     }
   } 
   else if (rel==1) { //release 16 numbers
     vectEtaBinning = &m_Etabins;
     if (range==0) { //20-50 GeV region
       if (set==0 || set>2) {//Loose
	 std::cout << "egammaSFclass: ERROR : only Medium and Tight scale factors exist" << std::endl;
	 return make_pair(-1.,-1.);
       }
       else if (set==1) {//Medium
	 vectEff = &efficienciesRel16Medium2050;
	 vectUnc = &uncertaintiesRel16Medium2050;
       }
       else if (set==2) {//Tight
	 vectEff = &efficienciesRel16Tight2050;
	 vectUnc = &uncertaintiesRel16Tight2050;
       }
     }//endif 20-50 GeV
     else if (range==1) { //30-50 GeV region
       if (set==0 || set>2) {//Loose
	 std::cout << "egammaSFclass: ERROR : only Medium and Tight scale factors exist" << std::endl;
	 return make_pair(-1.,-1.);
       }
       else if (set==1) {//Medium
	 vectEff = &efficienciesRel16Medium3050;
	 vectUnc = &uncertaintiesRel16Medium3050;
       }
       else if (set==2) {//Tight
	 vectEff = &efficienciesRel16Tight3050;
	 vectUnc = &uncertaintiesRel16Tight3050;
       }
     }//endif 30-50 GeV
     else {
	 std::cout << "egammaSFclass: ERROR : invalid range" << std::endl;
	 return make_pair(-1.,-1.);
     }
   }
   else { //release 15 numbers
     vectEtaBinning = &m_Etabins;
     if (range==0) { //20-50 GeV region
       if (set==0) {//Loose
	 vectEff = &efficienciesRel15Loose2050;
	 vectUnc = &uncertaintiesRel15Loose2050;
       }
       else if (set==1) {//Medium
	 vectEff = &efficienciesRel15Medium2050;
	 vectUnc = &uncertaintiesRel15Medium2050;
       }
       else if (set==2) {//Tight
	 vectEff = &efficienciesRel15Tight2050;
	 vectUnc = &uncertaintiesRel15Tight2050;
       }
       else {
	 std::cout << "egammaSFclass: ERROR : invalid set of cuts" << std::endl;
	 return make_pair(-1.,-1.);
       }
     }//endif 20-50 GeV
     else if (range==1) { //30-50 GeV region
       if (set==0) {//Loose
	 vectEff = &efficienciesRel15Loose3050;
	 vectUnc = &uncertaintiesRel15Loose3050;
       }
       else if (set==1) {//Medium
	 vectEff = &efficienciesRel15Medium3050;
	 vectUnc = &uncertaintiesRel15Medium3050;
       }
       else if (set==2) {//Tight
	 vectEff = &efficienciesRel15Tight3050;
	 vectUnc = &uncertaintiesRel15Tight3050;
       }
       else {
	 std::cout << "egammaSFclass: ERROR : invalid set of cuts" << std::endl;
	 return make_pair(-1.,-1.);
       }
     }//endif 30-50 GeV
     else {
	 std::cout << "egammaSFclass: ERROR : invalid range" << std::endl;
	 return make_pair(-1.,-1.);
     }
   }//endif rel15

   //Choice of the eta bin
   int ietabin=-1;
   while (ietabin<((int)vectEtaBinning->size()-1) && eta>=vectEtaBinning->at(ietabin+1)) ietabin++;
   if (ietabin<0 || ietabin>=((int)vectEtaBinning->size()-1)) {
     std::cout << "egammaSFclass: ERROR : given eta value outside range of existing scale factors" << std::endl;
     return make_pair(-1.,-1.);
   }


   float effvseta = vectEff->at(ietabin)/100.;
   float uncvseta = vectUnc->at(ietabin)/100.;

   float eff = effvseta;
   float unc = uncvseta;

   if (etcorrection) {
     std::pair<float,float> corr = etCorrection(ET, set, rel);
     unc = eff*corr.first * sqrt( unc*unc/eff/eff + corr.second*corr.second/corr.first/corr.first );
     eff *= corr.first;
   }

   return make_pair(eff,unc);
}


//Returns the ET-correction factor (and uncertainty) to the scale factor for the correspond ET bin and Medium (set=1) or Tight (set=2)
std::pair<float,float> egammaSFclass::etCorrection(float ET, int set, int rel) {
  //for backport of rel16 SF-ET-dependence to rel15
  if (rel==0) rel=1;  
  
  std::vector<float> * vectCorr=0;
  std::vector<float> * vectUncCorr=0;
  std::vector<float> * vectETBinning=0;
  vectETBinning = &m_ETbins;
  
  if (set==0) {//Loose
    std::cout << "egammaSFclass: ERROR : ET-correction factors not implemented for Loose" << std::endl;
    return make_pair(-1.,-1.);
  }
  else if (set==1) {//Medium
    if (rel==1) {
      vectCorr = &ETCorrectionsMediumRel16;
      vectUncCorr = &uncertaintiesETCorrectionsMediumRel16;
    }
    else if (rel==2) {
      vectCorr = &ETCorrectionsMediumRel166Data2010;
      vectUncCorr = &uncertaintiesETCorrectionsMediumRel166Data2010;
    }
    else if (rel==3) {
      vectCorr = &ETCorrectionsMediumRel166EPS;
      vectUncCorr = &uncertaintiesETCorrectionsMediumRel166EPS;
    }
    else if (rel==4) {
      vectETBinning = &m_ETbinsFullRange;
      vectCorr = &ETCorrectionsMediumRel166EPSFullRange;
      vectUncCorr = &uncertaintiesETCorrectionsMediumRel166EPSFullRange;
    }
  }
  else if (set==2) {//Tight
    if (rel==1) {
      vectCorr = &ETCorrectionsTightRel16;
      vectUncCorr = &uncertaintiesETCorrectionsTightRel16;
    }
    else if (rel==2) {
      vectCorr = &ETCorrectionsTightRel166Data2010;
      vectUncCorr = &uncertaintiesETCorrectionsTightRel166Data2010;
    }
    else if (rel==3) {
      vectCorr = &ETCorrectionsTightRel166EPS;
      vectUncCorr = &uncertaintiesETCorrectionsTightRel166EPS;
    }
    else if (rel==4) {
      vectETBinning = &m_ETbinsFullRange;
      vectCorr = &ETCorrectionsTightRel166EPSFullRange;
      vectUncCorr = &uncertaintiesETCorrectionsTightRel166EPSFullRange;
    }
  }

  int iETbin=-1;
  while (iETbin<m_nETbins && ET>=vectETBinning->at(iETbin+1)) iETbin++;
  if (iETbin<0 || iETbin>=m_nETbins) {
    std::cout << "egammaSFclass: ERROR : given ET value (" << ET << ") outside range of existing ET-correction factors" << std::endl;
    return make_pair(-1.,-1.);
  }

  float eff=vectCorr->at(iETbin)/100.;
  float unc=vectUncCorr->at(iETbin)/100.;
  return make_pair(eff, unc);
}

