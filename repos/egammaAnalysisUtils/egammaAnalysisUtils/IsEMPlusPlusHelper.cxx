/********************************************************************

    Name:     IsEMPlusPlusHelper.cxx
    Package:  offline/Reconstruction/egamma/egammaAnalysis/egammaAnalysisUtils

    Authors:  John Alison <john.alison@cern.ch>
              Chris Lester <clester@sas.upenn.edu>

    Created:  June 2011
    Comment:  Athena Wrapper for IsEMPlusPlusDefs.cxx 

    Includes:
     
     Tight++ Optimization for  > 20 GeV electrons (MC corrected from Z T and P)
     Medium++ Optimization for  > 20 GeV electrons (MC corrected from Z T and P)
	   Loose++  Optimization for  > 20 GeV electrons (MC corrected from Z T and P)
	   
	   Tight++ Optimization  for 10-20 GeV electrons (MC corrected from Tight Ele )
     Medium++ Optimization for 10-20 GeV electrons (MC corrected from Tight Ele )
	   Loose++ Optimization  for 10-20 GeV electrons (MC corrected from Tight Ele )
	   
    Usage:
      The IsEMTightPlusPlus, IsMediumPlusPlus, and IsLoosePlusPlus methods take an egamma object
       and returns true if the electron satisfies the loose++ or medium++ requriements.
       It returns false otherwise.

     Additional output will be givedn if debug is set, (false by default).
     
     The trigger bit emulates the online selction of e20_medium1.

   Created:
      June 2011

*********************************************************************/
#include "egammaAnalysisUtils/IsEMPlusPlusHelper.h"
#include "egammaAnalysisUtils/IsEMPlusPlusDefs.h"
// ====================================================================
bool isEMPlusPlusHelper::IsLoosePlusPlus(const egamma* eg,
					 bool debug,
					 bool isTrigger){
  
    
    if (!eg) {
      std::cout << "Failed, no egamma object. " << std::endl;
      return false; 
    }
    const CaloCluster* cluster = eg->cluster();
    if(!cluster){
      if(debug)
	std::cout << "Failed, no cluster. " << std::endl;
      return false; 
    }  

    float eta = fabs(cluster->etaBE(2)); 
    if(eta > 2.47){
      if(debug)
	std::cout << "Failed, eta range. " << std::endl;
      return false;
    }

    float et = cluster->energy()/cosh(eta); 

    float e237   = eg->detailValue(egammaParameters::e237);
    float e277   = eg->detailValue(egammaParameters::e277);
    float Reta = e277 != 0 ? e237/e277 : 0.;
    float weta2c = eg->detailValue(egammaParameters::weta2);

    double ethad1 = eg->detailValue(egammaParameters::ethad1);
    double ethad = eg->detailValue(egammaParameters::ethad);
    double raphad1 = fabs(et) != 0. ? ethad1/et : 0.;
    double raphad  = fabs(et) != 0. ? ethad/et : 0.;
  
    // E of 2nd max between max and min in strips
    double emax2  = eg->detailValue(egammaParameters::e2tsts1);
    // E of 1st max in strips
    double emax   = eg->detailValue(egammaParameters::emaxs1);

    // fraction of energy reconstructed in the 1st sampling
    double f1     = eg->detailValue(egammaParameters::f1);
    
    // E of 1st max in strips
    double wtot   = eg->detailValue(egammaParameters::wtots1);
    
    // (Emax1-Emax2)/(Emax1+Emax2)
    double demaxs1 = (emax+emax2)==0. ? 0 : (emax-emax2)/(emax+emax2);
    
    // number of precision hits (Pixels+SCT)
    int nSi = 0;
    int nPi = 0;
    int nSiOutliers = 0; 
    int nPiOutliers = 0; 

    // retrieve associated track
    const Rec::TrackParticle* track  = eg->trackParticle();    

    if (track) {
     const Trk::TrackSummary* summary = track->trackSummary();

      if (summary) {
        nPi = summary->get(Trk::numberOfPixelHits);
        nSi = summary->get(Trk::numberOfPixelHits)+summary->get(Trk::numberOfSCTHits);
        nPiOutliers = summary->get(Trk::numberOfPixelOutliers);	
        nSiOutliers = summary->get(Trk::numberOfPixelOutliers)+summary->get(Trk::numberOfSCTOutliers);
        
        }
    } 
    else {
      std::cout << "Failed, no track particle: et= " << et << "eta= " << eta << std::endl;
    }


    // delta eta
    double deltaEta = fabs(eg->detailValue(egammaParameters::deltaEta1));

    bool result = isLoosePlusPlus(eta,et,
				  raphad,raphad1,Reta,weta2c,
				  f1,wtot,demaxs1,deltaEta,nSi,nSiOutliers,
          nPi, nPiOutliers,
				  debug,isTrigger);
				  
    if (debug)
    {

      std::cout << "rhad= "     << raphad  << "  " << raphad1 << std::endl;
      std::cout << "reta= "     << Reta  << std::endl;
      std::cout << "wstot= "    << wtot  << std::endl;
      std::cout << "weta2= "    << weta2c  << std::endl;
      std::cout << "eratio= "   << demaxs1  << std::endl;
      std::cout << "npix= "     << nPi + nPiOutliers  << std::endl;
      std::cout << "nsi= "      << nSi + nSiOutliers  << std::endl; 
      std::cout << "deltaEta= "      << deltaEta  << std::endl;
    }

    return result;
}

// ====================================================================
bool isEMPlusPlusHelper::IsMediumPlusPlus(const egamma* eg, 
					  bool debug,
					  bool isTrigger){

					    
    
    const CaloCluster* cluster = eg->cluster();
    if(!cluster){
      if(debug)
	std::cout << "Failed, no cluster. " << std::endl;
      return false;
    }  

    float eta = fabs(cluster->etaBE(2)); //where cluster is the CaloCluster
    if(eta > 2.47){
      if(debug)
	std::cout << "Failed, eta range. " << std::endl;
      return false;
    }

    float et = cluster->energy()/cosh(eta); //where cluster is the CaloCluster
    if(et < 10*1000){
      if(debug)
	std::cout << "Failed, Et below 10 GeV. " << std::endl;
      return false;
    }

    float e237   = eg->detailValue(egammaParameters::e237);
    float e277   = eg->detailValue(egammaParameters::e277);
    float Reta = e277 != 0 ? e237/e277 : 0.;         
    float weta2c = eg->detailValue(egammaParameters::weta2);

    double ethad1 = eg->detailValue(egammaParameters::ethad1);
    double ethad = eg->detailValue(egammaParameters::ethad);
    double raphad1 = fabs(et) != 0. ? ethad1/et : 0.;
    double raphad  = fabs(et) != 0. ? ethad/et : 0.; 
  
    // E of 2nd max between max and min in strips
    double emax2  = eg->detailValue(egammaParameters::e2tsts1);
    // E of 1st max in strips
    double emax   = eg->detailValue(egammaParameters::emaxs1);

    // fraction of energy reconstructed in the 1st sampling
    double f1     = eg->detailValue(egammaParameters::f1);
    
    // E of 1st max in strips
    double wtot   = eg->detailValue(egammaParameters::wtots1);
    
    // (Emax1-Emax2)/(Emax1+Emax2)
    double demaxs1 = (emax+emax2)==0. ? 0 : (emax-emax2)/(emax+emax2);

    // retrieve associated track
    const Rec::TrackParticle* track  = eg->trackParticle();    

    // retrieve summary
    const Trk::TrackSummary* summary = track->trackSummary();

    // Track quality cut
    // number of B-layer hits
    int nBL = 0;
    int nBLOutliers = 0;
    // number of Pixel hits
    int nPi = 0;
    int nPiOutliers = 0;
    // number of precision hits (Pixels+SCT)
    int nSi = 0;
    int nSiOutliers = 0; 
    int nTRThigh          = 0;
    int nTRThighOutliers  = 0;
    int nTRT         = 0;
    int nTRTOutliers = 0;

    if (summary) {
      nBL = summary->get(Trk::numberOfBLayerHits);
      nBLOutliers = summary->get(Trk::numberOfBLayerOutliers);
      nPi = summary->get(Trk::numberOfPixelHits);
      nSi = summary->get(Trk::numberOfPixelHits)+summary->get(Trk::numberOfSCTHits);
      nPiOutliers = summary->get(Trk::numberOfPixelOutliers);	
      nTRThigh          = summary->get(Trk::numberOfTRTHighThresholdHits);
      nTRThighOutliers  = summary->get(Trk::numberOfTRTHighThresholdOutliers);
      nTRT         = summary->get(Trk::numberOfTRTHits);
      nTRTOutliers = summary->get(Trk::numberOfTRTOutliers); 
      nSiOutliers = summary->get(Trk::numberOfPixelOutliers)+summary->get(Trk::numberOfSCTOutliers);
    } 

    // define EMTrackMatch object
    bool expectHitInBLayer = eg->detailValue(egammaParameters::expectHitInBLayer);

    // delta eta
    double deltaEta = fabs(eg->detailValue(egammaParameters::deltaEta1));

    // transverse impact parameter
    double trackd0 = fabs(eg->detailValue(egammaParameters::trackd0_physics));

    double rTRT = (nTRT+nTRTOutliers) > 0 ? ((double)(nTRThigh+nTRThighOutliers)/(nTRT+nTRTOutliers) ) : 0.;
    
    bool result = isMediumPlusPlus(eta,et,
				   raphad,raphad1,Reta,weta2c,
				   f1,wtot,demaxs1,deltaEta,trackd0,
				   rTRT,nTRT,nTRTOutliers,
				   nSi,nSiOutliers,nPi,nPiOutliers,
				   nBL,nBLOutliers,expectHitInBLayer, 
				   debug,isTrigger);


    if (debug)
    {

      std::cout << "rhad= "     << raphad  << "  " << raphad1 << std::endl;
      std::cout << "reta= "     << Reta  << std::endl;
      std::cout << "wstot= "    << wtot  << std::endl;
      std::cout << "weta2= "    << weta2c  << std::endl;
      std::cout << "eratio= "   << demaxs1  << std::endl;
      std::cout << "deltaeta= " << deltaEta  << std::endl;
      std::cout << "npix= "     << nPi + nPiOutliers  << std::endl;
      std::cout << "nsi= "      << nSi + nSiOutliers  << std::endl;
      std::cout << "nbl= "      << nBL + nBLOutliers  << std::endl;
      std::cout << "A0= "       << trackd0  << std::endl;
      std::cout << "TR = "      << rTRT << std::endl;

    } 

    return result;
}
// ====================================================================
bool isEMPlusPlusHelper::IsTightPlusPlus(const egamma* eg,  
					  bool debug,
					  bool isTrigger){

					    
    const CaloCluster* cluster = eg->cluster();
    if(!cluster){
      if(debug)
	std::cout << "Failed, no cluster. " << std::endl;
      return false;
    }  

    float eta = fabs(cluster->etaBE(2)); //where cluster is the CaloCluster
    if(eta > 2.47){
      if(debug)
	std::cout << "Failed, eta range. " << std::endl;
      return false;
    }

    float et = cluster->energy()/cosh(eta); //where cluster is the CaloCluster
    if(et < 10*1000){
      if(debug)
	std::cout << "Failed, Et below 10 GeV. " << std::endl;
      return false;
    }

    float e237   = eg->detailValue(egammaParameters::e237);
    float e277   = eg->detailValue(egammaParameters::e277);
    float Reta = e277 != 0 ? e237/e277 : 0.;         
    float weta2c = eg->detailValue(egammaParameters::weta2);

    double ethad1 = eg->detailValue(egammaParameters::ethad1);
    double ethad = eg->detailValue(egammaParameters::ethad);
    double raphad1 = fabs(et) != 0. ? ethad1/et : 0.;
    double raphad  = fabs(et) != 0. ? ethad/et : 0.; 
  
    // E of 2nd max between max and min in strips
    double emax2  = eg->detailValue(egammaParameters::e2tsts1);
    // E of 1st max in strips
    double emax   = eg->detailValue(egammaParameters::emaxs1);

    // fraction of energy reconstructed in the 1st sampling
    double f1     = eg->detailValue(egammaParameters::f1);
    
    // E of 1st max in strips
    double wtot   = eg->detailValue(egammaParameters::wtots1);
    
    // (Emax1-Emax2)/(Emax1+Emax2)
    double demaxs1 = (emax+emax2)==0. ? 0 : (emax-emax2)/(emax+emax2);

    // retrieve associated track
    const Rec::TrackParticle* track  = eg->trackParticle();    

    // retrieve summary
    const Trk::TrackSummary* summary = track->trackSummary();

    // Track quality cut
    // number of B-layer hits
    int nBL = 0;
    int nBLOutliers = 0;
    // number of Pixel hits
    int nPi = 0;
    int nPiOutliers = 0;
    // number of precision hits (Pixels+SCT)
    int nSi = 0;
    int nSiOutliers = 0; 
    int nTRThigh          = 0;
    int nTRThighOutliers  = 0;
    int nTRT         = 0;
    int nTRTOutliers = 0;

    if (summary) {
      nBL = summary->get(Trk::numberOfBLayerHits);
      nBLOutliers = summary->get(Trk::numberOfBLayerOutliers);
      nPi = summary->get(Trk::numberOfPixelHits);
      nSi = summary->get(Trk::numberOfPixelHits)+summary->get(Trk::numberOfSCTHits);
      nPiOutliers = summary->get(Trk::numberOfPixelOutliers);	
      nTRThigh          = summary->get(Trk::numberOfTRTHighThresholdHits);
      nTRThighOutliers  = summary->get(Trk::numberOfTRTHighThresholdOutliers);
      nTRT         = summary->get(Trk::numberOfTRTHits);
      nTRTOutliers = summary->get(Trk::numberOfTRTOutliers); 
      nSiOutliers = summary->get(Trk::numberOfPixelOutliers)+summary->get(Trk::numberOfSCTOutliers);
    } 

    // define EMTrackMatch object
    bool expectHitInBLayer = eg->detailValue(egammaParameters::expectHitInBLayer);

    // delta eta and delta phi
    double deltaEta = fabs(eg->detailValue(egammaParameters::deltaEta1));
    double deltaphi = eg->detailValue(egammaParameters::deltaPhi2);
    
    
    // E/p
    const Rec::TrackParticle* t  = eg->trackParticle();    
    double trackp = 0; 
    if (t) trackp = t->p();
    double ep = 0.;
    if (fabs(trackp)>0.) ep = eg->cluster()->energy()/trackp;
  

    // transverse impact parameter
    double trackd0 = fabs(eg->detailValue(egammaParameters::trackd0_physics));

    double rTRT = (nTRT+nTRTOutliers) > 0 ? ((double)(nTRThigh+nTRThighOutliers)/(nTRT+nTRTOutliers) ) : 0.;
    
    // test conversion bit from isEM word
    
    double convBit = eg->isem(egammaPID::CONVMATCH_ELECTRON);
   
    
    bool result = isTightPlusPlus(eta,et,
				   raphad,raphad1,Reta,weta2c,
				   f1,wtot,demaxs1,deltaEta,trackd0,
				   rTRT,nTRT,nTRTOutliers,
				   nSi,nSiOutliers,nPi,nPiOutliers,
				   nBL,nBLOutliers,expectHitInBLayer, ep, deltaphi,
				   convBit, debug,isTrigger);
	
    if (debug)
    {

      std::cout << "rhad= "     << raphad  << "  " << raphad1 << std::endl;
      std::cout << "reta= "     << Reta  << std::endl;
      std::cout << "wstot= "    << wtot  << std::endl;
      std::cout << "weta2= "    << weta2c  << std::endl;
      std::cout << "eratio= "   << demaxs1  << std::endl;
      std::cout << "deltaphi= " << deltaphi  << std::endl;
      std::cout << "deltaeta= " << deltaEta  << std::endl;
      std::cout << "ep= "       << ep  << std::endl;
      std::cout << "npix= "     << nPi + nPiOutliers  << std::endl;
      std::cout << "nsi= "      << nSi + nSiOutliers  << std::endl;
      std::cout << "nbl= "      << nBL + nBLOutliers  << std::endl;
      std::cout << "A0= "       << trackd0  << std::endl;
      std::cout << "Conv = "    << convBit << std::endl;
      std::cout << "TR = "      << rTRT << std::endl;
      std::cout << "nTRT = "      << nTRT + nTRTOutliers << std::endl;
    } 


    return result;
}


