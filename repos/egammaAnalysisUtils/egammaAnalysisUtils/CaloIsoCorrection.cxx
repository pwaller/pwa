#include <iostream>
#include <cmath>

#include "egammaAnalysisUtils/CaloIsoCorrection.h"

using namespace CaloIsoCorrection;

const float GeV = 1000.;

//-----------------------------------------------------------------------
//
// Internal Methods
//
namespace CaloIsoCorrection{
  float GetPtCorrection       (float energy, float etaS2, float etaPointing, float etaCluster, 
                               float radius, bool is_mc=true, 
                               bool isConversion=false, ParticleType parttype = ELECTRON);
  float GetPtCorrectionError  (float energy, float etaS2, float etaPointing, float etaCluster, 
                               float radius, bool is_mc=true, ParticleType parttype = ELECTRON);

  int GetRadius(float radius);
  int GetEtaBinFine(float eta);
  int GetEtaBinCoarse(float eta);
  
  float GetPtCorrectionFactor(float eta,  
                            const float* mc_leakage_corrections_ptr = 0, 
                            const float* data_leakage_corrections_ptr = 0);
  float GetPtCorrectionValue(float energy, float etaPointing, float etaCluster, float scale_factor);

  float GetNPVCorrection (float eta, float radius, unsigned int nPV, bool is_mc, ParticleType parttype = ELECTRON);
  float GetNPVCorrectionError (float eta, float radius, unsigned int nPV, bool is_mc, ParticleType parttype = ELECTRON);

  float GetEDCorrection (float Etcone40, float Etcone40_ED_corrected, float radius);

  // array sizes
  const unsigned int nBinsEtaFine = 11;
  const unsigned int nBinsEtaCoarse = 5;
  
  // eta bins
  const float eta_bins_fine[nBinsEtaFine+1] = {0.0, 0.10, 0.60, 0.80, 1.15, 1.37, 1.52, 1.81, 2.01, 2.37, 2.47, 5.00};
  const float eta_bins_coarse[nBinsEtaCoarse+1] = {0.0, 0.60, 1.37, 1.52, 1.81, 2.47};

  // OLD isolation corrections: fine grained in eta, derived from MC
  const float old_mc_leakage_corrections_photon_20[] = {0.014582 , 0.013887 , 0.013786, 0.017952 , 0.020799 , 0.022892 , 0.022947 , 0.027274, 0.034607 , 0.04111  , 0.043765 };
  const float old_mc_leakage_corrections_photon_30[] = {0.0149955, 0.0143672, 0.01439 , 0.0189413, 0.0221763, 0.0251387, 0.0244524, 0.028928, 0.0373025, 0.044983 , 0.0450644};
  const float old_mc_leakage_corrections_photon_40[] = {0.0150641, 0.0144416, 0.014464, 0.0191335, 0.0224708, 0.0256225, 0.0248054, 0.029223, 0.0378147, 0.0457925, 0.0457752};

  const float old_mc_leakage_corrections_electron_20[] = {0.0146779, 0.0140476, 0.0142736, 0.0187919, 0.0242244, 0.0327271, 0.0236067, 0.0273382, 0.0347824, 0.0405783, 0.0488965};
  const float old_mc_leakage_corrections_electron_30[] = {0.0151632, 0.0145416, 0.0149607, 0.0198783, 0.0258172, 0.0404185, 0.0257027, 0.0289142, 0.0375322, 0.0451606, 0.0555181};
  const float old_mc_leakage_corrections_electron_40[] = {0.0152929, 0.0146146, 0.0150541, 0.0200918, 0.0261464, 0.043179 , 0.0262671, 0.0292846, 0.0380784, 0.0462397, 0.056945 };
  

  // NEW isolation corrections: fine grained in eta, derived from MC
  const float mc_leakage_corrections_electron_15[] = {0.0134623, 0.0125705, 0.0127194, 0.016388 , 0.0192139, 0.0191176, 0.019365 , 0.0224323, 0.0276738, 0.0306204, 0.0395363};
  const float mc_leakage_corrections_electron_20[] = {0.0146765, 0.0137598, 0.0141393, 0.0185445, 0.0222504, 0.0303701, 0.022529 , 0.0255273, 0.0322996, 0.0367724, 0.0488965};
  const float mc_leakage_corrections_electron_25[] = {0.0150446, 0.0141208, 0.0146059, 0.0192928, 0.0233765, 0.0355231, 0.0239549, 0.0266049, 0.0340472, 0.0395156, 0.0533984};
  const float mc_leakage_corrections_electron_30[] = {0.0151549, 0.0142345, 0.0147978, 0.0195921, 0.0238402, 0.0374921, 0.0245635, 0.0270403, 0.0347653, 0.0407656, 0.0555181};
  const float mc_leakage_corrections_electron_35[] = {0.0151991, 0.0142886, 0.0148807, 0.0197355, 0.0240916, 0.0389585, 0.024845 , 0.0272151, 0.0350951, 0.0414101, 0.0565319};
  const float mc_leakage_corrections_electron_40[] = {0.0152502, 0.014324 , 0.014922 , 0.019808 , 0.0242069, 0.0398394, 0.0250683, 0.0273238, 0.0352379, 0.0417484, 0.056945 };

  const float mc_leakage_corrections_photon_converted_15[] = {0.0124144, 0.0117418, 0.0122051, 0.0159856, 0.0189189, 0.0190803, 0.0195599, 0.0230894, 0.0287442, 0.0335009, 0.040739 };
  const float mc_leakage_corrections_photon_converted_20[] = {0.0134282, 0.0127686, 0.0134831, 0.0180318, 0.0218801, 0.030747 , 0.0227755, 0.0262832, 0.0335691, 0.0401866, 0.043765 };
  const float mc_leakage_corrections_photon_converted_25[] = {0.0136567, 0.0130497, 0.0138831, 0.0187274, 0.0229529, 0.0360431, 0.0242219, 0.0274141, 0.0354121, 0.0432104, 0.0450998};
  const float mc_leakage_corrections_photon_converted_30[] = {0.0137181, 0.0131058, 0.0140011, 0.0189988, 0.023384 , 0.038064 , 0.0248426, 0.0278485, 0.0361593, 0.044579 , 0.0450644};
  const float mc_leakage_corrections_photon_converted_35[] = {0.0137829, 0.0131081, 0.01406  , 0.019133 , 0.0235932, 0.0396043, 0.0251306, 0.0280451, 0.0365044, 0.0452737, 0.0452159};
  const float mc_leakage_corrections_photon_converted_40[] = {0.0137756, 0.0131087, 0.0140897, 0.0192113, 0.0237036, 0.0405692, 0.0253519, 0.0281581, 0.0366884, 0.0456197, 0.0457752};

  const float mc_leakage_corrections_photon_unconverted_15[] = {0.0136592, 0.0127361, 0.0122583, 0.0152527, 0.0170659, 0.0157067, 0.0195983, 0.0242494, 0.0287865, 0.033302 , 0.040739 };
  const float mc_leakage_corrections_photon_unconverted_20[] = {0.0148505, 0.0139408, 0.0135913, 0.0171323, 0.0196672, 0.0254563, 0.021963 , 0.0274632, 0.0335511, 0.039913 , 0.043765 };
  const float mc_leakage_corrections_photon_unconverted_25[] = {0.0152095, 0.0143039, 0.0140069, 0.0177627, 0.0206302, 0.029655 , 0.0229128, 0.0285693, 0.0353589, 0.0428317, 0.0450998};
  const float mc_leakage_corrections_photon_unconverted_30[] = {0.0153482, 0.0144291, 0.0141718, 0.018018 , 0.0210249, 0.0312614, 0.0232916, 0.028999 , 0.0361068, 0.0442073, 0.0450644};
  const float mc_leakage_corrections_photon_unconverted_35[] = {0.0153847, 0.0144704, 0.0142212, 0.0181336, 0.0212057, 0.032474 , 0.0234635, 0.0291766, 0.0364465, 0.0448465, 0.0452159};
  const float mc_leakage_corrections_photon_unconverted_40[] = {0.0154202, 0.0144914, 0.0142582, 0.0181816, 0.0213156, 0.0331942, 0.0235738, 0.0292826, 0.0365929, 0.0451769, 0.0457752};


  // additional isolation corrections: coarse grained in eta, measured with 2010 data
//  const float data_leakage_corrections_photon_40  [] = {.0030, .0044, 0., .0012, .0041};
//   const float data_leakage_corrections_electron_20[] = {.0040, .0074, 0., .0075, .0064};
//   const float data_leakage_corrections_electron_30[] = {.0041, .0072, 0., .0094, .0023};
//   const float data_leakage_corrections_electron_40[] = {.0042, .0072, 0., .0111, .0038};

  // additional isolation correction errors: coarse grained in eta, measured with 2010 data
//   const float data_leakage_corrections_error_photon_40  [] = {.0013, .0012, 0., .0019, .0014};
//   const float data_leakage_corrections_error_electron_20[] = {.0010, .0011, 0., .0047, .0019};
//   const float data_leakage_corrections_error_electron_30[] = {.0018, .0016, 0., .0069, .0026};
//   const float data_leakage_corrections_error_electron_40[] = {.0026, .0033, 0., .0062, .0038};
  
  // additional isolation corrections: coarse grained in eta, measured with 2011 periods B-E
  const float data_leakage_corrections_photon_20  [] = {.0032, .0073, 0., .0046, .0082};
  const float data_leakage_corrections_photon_30  [] = {.0036, .0086, 0., .0044, .0086};
  const float data_leakage_corrections_photon_40  [] = {.0040, .0101, 0., .0048, .0079};
  
  const float data_leakage_corrections_electron_20[] = {.0042, .0087, 0., .0128, .0114};
  const float data_leakage_corrections_electron_30[] = {.0058, .0119, 0., .0142, .0130};
  const float data_leakage_corrections_electron_40[] = {.0062, .0168, 0., .0170, .0147};

  // additional isolation correction errors: coarse grained in eta, measured with 2011 periods B-E
  const float data_leakage_corrections_error_photon_20  [] = {.0005, .0009, 0., .0012, .0013};
  const float data_leakage_corrections_error_photon_30  [] = {.0006, .0012, 0., .0016, .0017};
  const float data_leakage_corrections_error_photon_40  [] = {.0010, .0019, 0., .0020, .0019};
  
  const float data_leakage_corrections_error_electron_20[] = {.0008, .0012, 0., .0024, .0016};
  const float data_leakage_corrections_error_electron_30[] = {.0029, .0018, 0., .0032, .0025};
  const float data_leakage_corrections_error_electron_40[] = {.0040, .0026, 0., .0049, .0027};
  
  // nPV pileup corrections, derived on data (2011, periods D,E)
  //   checked on mc10a (75ns spacing) - results are close to electrons, within errors
  // UNITS ARE GEV!
  // >= 2 tracks/vertex
  const float mc_npv_corrections_20[] = {0.053, 0.059, 0.0, 0.070, 0.076};
  const float mc_npv_corrections_30[] = {0.145, 0.163, 0.0, 0.175, 0.189};
  const float mc_npv_corrections_40[] = {0.280, 0.306, 0.0, 0.331, 0.351};
  
  // nPV pileup corrections, derived on data (2011, periods D,E)
  // UNITS ARE GEV!
  // >= 2 tracks/vertex
  const float data_npv_corrections_20[] = {0.053, 0.059, 0.0, 0.070, 0.076};
  const float data_npv_corrections_30[] = {0.145, 0.163, 0.0, 0.175, 0.189};
  const float data_npv_corrections_40[] = {0.280, 0.306, 0.0, 0.331, 0.351};
  
  // errors (relative) for nPV pileup corrections
  // - dominant source of errors are: run-to-run and bunch-to-bunch variation in 2011 data
  const float npv_corrections_relative_error_20[] = {0.38, 0.38, 0.0, 0.38, 0.38};
  const float npv_corrections_relative_error_30[] = {0.28, 0.38, 0.0, 0.38, 0.38};
  const float npv_corrections_relative_error_40[] = {0.30, 0.30, 0.0, 0.30, 0.30};
}
//-----------------------------------------------------------------------
  

//-----------------------------------------------------------------------
// User function
// Returns the nPV corrected isolation
//
float CaloIsoCorrection::GetNPVCorrectedIsolation(unsigned int nPV,
                                                  float etaS2,
                                                  float radius,
                                                  bool is_mc,
                                                  float Etcone_value,
                                                  ParticleType parttype) {
  
  float npv_correction = GetNPVCorrection(etaS2, radius, nPV, is_mc, parttype);
  return Etcone_value - npv_correction;
}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
// User function
// Returns the ED corrected isolation
//
float CaloIsoCorrection::GetEDCorrectedIsolation(float Etcone40,
                                                 float Etcone40_ED_corrected,
                                                 float radius,
                                                 float Etcone_value,
                                                 ParticleType /*parttype*/) {
  
  float ED_correction = GetEDCorrection(Etcone40, Etcone40_ED_corrected, radius);
  return Etcone_value - ED_correction;
}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
// User function
// Returns the pt leakage corrected isolation
//
float CaloIsoCorrection::GetPtCorrectedIsolation(float energy, 
                                                 float etaS2, 
                                                 float etaPointing, 
                                                 float etaCluster, 
                                                 float radius, 
                                                 bool is_mc, 
                                                 float Etcone_value,
                                                 bool isConversion,
                                                 ParticleType parttype){
  
  float pt_correction = GetPtCorrection(energy, etaS2, etaPointing, etaCluster, radius, is_mc, isConversion, parttype);
  return Etcone_value - pt_correction;
}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
// User function
// Returns the pt leakage + nPV corrected isolation
//
float CaloIsoCorrection::GetPtNPVCorrectedIsolation(unsigned int nPV,
                                                    float energy, 
                                                    float etaS2, 
                                                    float etaPointing, 
                                                    float etaCluster, 
                                                    float radius, 
                                                    bool is_mc, 
                                                    float Etcone_value,
                                                    bool isConversion,
                                                    ParticleType parttype){
  
  float pt_correction = GetPtCorrection(energy, etaS2, etaPointing, etaCluster, radius, is_mc, isConversion, parttype);
  float npv_correction = GetNPVCorrection(etaS2, radius, nPV, is_mc, parttype);
  return Etcone_value - pt_correction - npv_correction;
}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
// User function
// Returns the pt leakage + energy density corrected isolation
//
float CaloIsoCorrection::GetPtEDCorrectedIsolation(float Etcone40,
                                                   float Etcone40_ED_corrected,
                                                   float energy, 
                                                   float etaS2, 
                                                   float etaPointing, 
                                                   float etaCluster, 
                                                   float radius, 
                                                   bool is_mc, 
                                                   float Etcone_value,
                                                   bool isConversion,
                                                   ParticleType parttype){
  
  float pt_correction = GetPtCorrection(energy, etaS2, etaPointing, etaCluster, radius, is_mc, isConversion, parttype);
  float ED_correction = GetEDCorrection(Etcone40, Etcone40_ED_corrected, radius);
  return Etcone_value - pt_correction - ED_correction;
}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
// User function
// Returns the error on the nPV pileup correction
//
float CaloIsoCorrection::GetNPVCorrectedIsolationError(unsigned int nPV,
                                                       float etaS2,
                                                       float radius,
                                                       bool is_mc,
                                                       ParticleType parttype){
  
  return GetNPVCorrectionError(etaS2, radius, nPV, is_mc, parttype);
}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
// User function
// Returns the error on the data-derived pT leakage correction
//
float CaloIsoCorrection::GetPtCorrectedIsolationError(float energy, 
                                                      float etaS2, 
                                                      float etaPointing, 
                                                      float etaCluster, 
                                                      float radius, 
                                                      bool is_mc,
                                                      ParticleType parttype){
  
  return GetPtCorrectionError(energy, etaS2, etaPointing, etaCluster, radius, is_mc, parttype);
}
//-----------------------------------------------------------------------




//***************************************************************************************************************************
//***************************************************************************************************************************
// Internal Functions Below.
//***************************************************************************************************************************
//***************************************************************************************************************************

//-----------------------------------------------------------------------
// Internal function
// Gets the pt correction factor
//
float CaloIsoCorrection::GetPtCorrection(float energy, 
                                             float etaS2, float etaPointing, float etaCluster, 
                                             float radius, 
                                             bool is_mc, 
                                             bool isConversion, ParticleType parttype){
  int newrad = GetRadius(radius);
  const float* mc_corrections_ptr(0);
  const float* data_corrections_ptr(0);
  switch(newrad){
    case 15: 
      if (parttype == PHOTON) {
        // photons
        if(isConversion) mc_corrections_ptr = (float*)mc_leakage_corrections_photon_converted_15; 
        else             mc_corrections_ptr = (float*)mc_leakage_corrections_photon_unconverted_15;
      } else {
        // electrons
        mc_corrections_ptr = (float*)mc_leakage_corrections_electron_15;
      }
      break;
    case 20: 
      if (parttype == PHOTON) {
        // photons
        if(isConversion) mc_corrections_ptr = (float*)mc_leakage_corrections_photon_converted_20; 
        else             mc_corrections_ptr = (float*)mc_leakage_corrections_photon_unconverted_20; 
      } else {
        // electrons
        mc_corrections_ptr = (float*)mc_leakage_corrections_electron_20;
      }
      if (!is_mc) {
        if (parttype == PHOTON) {
          // photons
          data_corrections_ptr = (float*)data_leakage_corrections_photon_20; 
        } else {
          // electrons
          data_corrections_ptr = (float*)data_leakage_corrections_electron_20; 
        }
      }
      break;
    case 25: 
      if (parttype == PHOTON) {
        // photons
        if(isConversion) mc_corrections_ptr = (float*)mc_leakage_corrections_photon_converted_25; 
        else             mc_corrections_ptr = (float*)mc_leakage_corrections_photon_unconverted_25; 
      } else {
        // electrons
        mc_corrections_ptr = (float*)mc_leakage_corrections_electron_25;
      }
      break;
    case 30: 
      if (parttype == PHOTON) {
        // photons
        if(isConversion) mc_corrections_ptr = (float*)mc_leakage_corrections_photon_converted_30; 
        else             mc_corrections_ptr = (float*)mc_leakage_corrections_photon_unconverted_30; 
      } else {
        // electrons
        mc_corrections_ptr = (float*)mc_leakage_corrections_electron_30;
      }
      if (!is_mc) {
        if (parttype == PHOTON) {
          // photons
          data_corrections_ptr = (float*)data_leakage_corrections_photon_30; 
        } else {
          // electrons
          data_corrections_ptr = (float*)data_leakage_corrections_electron_30; 
        }
      }
      break;
    case 35: 
      if (parttype == PHOTON) {
        // photons
        if(isConversion) mc_corrections_ptr = (float*)mc_leakage_corrections_photon_converted_35; 
        else             mc_corrections_ptr = (float*)mc_leakage_corrections_photon_unconverted_35; 
      } else {
        // electrons
        mc_corrections_ptr = (float*)mc_leakage_corrections_electron_35;
      }
      break;
    case 40: 
      if (parttype == PHOTON) {
        // photons
        if(isConversion) mc_corrections_ptr = (float*)mc_leakage_corrections_photon_converted_40; 
        else             mc_corrections_ptr = (float*)mc_leakage_corrections_photon_unconverted_40; 
      } else {
        // electrons
        mc_corrections_ptr = (float*)mc_leakage_corrections_electron_40;
      }
      if (!is_mc) {
        if (parttype == PHOTON) {
          // photons
          data_corrections_ptr = (float*)data_leakage_corrections_photon_40; 
        } else {
          // electrons
          data_corrections_ptr = (float*)data_leakage_corrections_electron_40; 
        }
      }
      break;
    default:
      std::cerr << "Unable to retrieve correction for cone with radius = " << radius << "." << std::endl
                << "--- Radii must be one of {.15, .20, .25, .30, .35, .40} OR {15, 20, 25, 30, 35, 40}." << std::endl;
      return 0.;
  }

  float scale_factor = GetPtCorrectionFactor(etaS2, mc_corrections_ptr, data_corrections_ptr);
  
  return GetPtCorrectionValue(energy, etaPointing, etaCluster, scale_factor);

}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
// Internal function
// Gets the photon correction
//
float CaloIsoCorrection::GetPtCorrectionError(float energy, 
                                                  float etaS2, float etaPointing, float etaCluster, 
                                                  float radius, 
                                                  bool is_mc,
                                                  ParticleType parttype){
  if (is_mc) return 0.;
  int newrad = GetRadius(radius);
  const float* data_corrections_ptr(0);
  switch(newrad){
    case 15: 
      break;
    case 20: 
      if (parttype == PHOTON) data_corrections_ptr = (float*)data_leakage_corrections_error_photon_20; 
      else data_corrections_ptr = (float*)data_leakage_corrections_error_electron_20; 
      break;
    case 25: 
      break;
    case 30: 
      if (parttype == PHOTON) data_corrections_ptr = (float*)data_leakage_corrections_error_photon_30; 
      else data_corrections_ptr = (float*)data_leakage_corrections_error_electron_30; 
      break;
    case 35: 
      break;
    case 40: 
      if (parttype == PHOTON) data_corrections_ptr = (float*)data_leakage_corrections_error_photon_40; 
      else data_corrections_ptr = (float*)data_leakage_corrections_error_electron_40; 
      break;
    default:
      std::cerr << "Unable to retrieve correction errors for cone with radius = " << radius << "." << std::endl
                << "--- Radii must be one of {.15, .20, .25, .30, .35, .40} OR {15, 20, 25, 30, 35, 40}." << std::endl;
      return 0.;
  }

  float scale_factor = GetPtCorrectionFactor(etaS2, 0, data_corrections_ptr);
  
  return GetPtCorrectionValue(energy, etaPointing, etaCluster, scale_factor);

}
//-----------------------------------------------------------------------


//-----------------------------------------------------------------------
// Internal function
// Used to retrieve the correct radius
int CaloIsoCorrection::GetRadius(float radius){
  int newrad = 0;
  // avoid roundoff errors by adding 0.1
  if(radius < 1)  newrad = (int)(radius * 100 + 0.1); 
  else            newrad = (int)radius;
  return newrad;
}
//-----------------------------------------------------------------------


//-----------------------------------------------------------------------
// Internal function
// Used to retrieve the correct (fine) eta bin number
//
int CaloIsoCorrection::GetEtaBinFine(float eta){
  int eta_bin=-1;
  float fabs_eta = fabs(eta);
  for (unsigned int i=0; i < nBinsEtaFine; ++i) {
    if ((fabs_eta >= eta_bins_fine[i]) && (fabs_eta < eta_bins_fine[i+1])) {
      eta_bin = i;
      break;
    }
  }
  return eta_bin;
}
//-----------------------------------------------------------------------


//-----------------------------------------------------------------------
// Internal function
// Used to retrieve the correct (coarse) eta bin number
//
int CaloIsoCorrection::GetEtaBinCoarse(float eta){
  int eta_bin=-1;
  float fabs_eta = fabs(eta);
  for (unsigned int i=0; i < nBinsEtaCoarse; ++i) {
    if ((fabs_eta >= eta_bins_coarse[i]) && (fabs_eta < eta_bins_coarse[i+1])) {
      eta_bin = i;
      break;
    }
  }
  return eta_bin;
}
//-----------------------------------------------------------------------


//-----------------------------------------------------------------------
// Internal function
// Returns the appropriate corrections value
//
float CaloIsoCorrection::GetPtCorrectionFactor(float eta,  
                                             const float* mc_leakage_corrections_ptr, 
                                             const float* data_leakage_corrections_ptr){
  if(!mc_leakage_corrections_ptr && !data_leakage_corrections_ptr) 
    return 0.;

  int eta_bin_fine = GetEtaBinFine(eta);
  int eta_bin_coarse = GetEtaBinCoarse(eta);
  
  float correction = 0.;
  if (mc_leakage_corrections_ptr && (eta_bin_fine >= 0)) correction += mc_leakage_corrections_ptr[eta_bin_fine];
  if (data_leakage_corrections_ptr && (eta_bin_coarse >= 0)) correction += data_leakage_corrections_ptr[eta_bin_coarse];

  return correction;
}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
// Internal function
// Does the final pt scaling
float CaloIsoCorrection::GetPtCorrectionValue(float energy, float etaPointing, float etaCluster, float scale_factor){
  // apply the correction to et
  double etaForPt = ((fabs(etaPointing - etaCluster) < 0.15) ? etaPointing : etaCluster);
  double et = (fabs(etaForPt)<99.) ? energy/cosh(etaForPt) : 0.;
  
  return scale_factor * et;
}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
// Internal function
// Returns an absolute correction based on number of vertices
float CaloIsoCorrection::GetNPVCorrection(float eta, float radius, unsigned int nPV, bool is_mc, ParticleType /*parttype*/){
  
  int newrad = GetRadius(radius);
  const float* npv_corrections_ptr(0);
  switch(newrad){
    case 15: 
      break;
    case 20: 
      if (is_mc) npv_corrections_ptr = (float*)mc_npv_corrections_20;
      else npv_corrections_ptr = (float*)data_npv_corrections_20; 
      break;
    case 25: 
      break;
    case 30: 
      if (is_mc) npv_corrections_ptr = (float*)mc_npv_corrections_30;
      else npv_corrections_ptr = (float*)data_npv_corrections_30; 
      break;
    case 35: 
      break;
    case 40: 
      if (is_mc) npv_corrections_ptr = (float*)mc_npv_corrections_40;
      else npv_corrections_ptr = (float*)data_npv_corrections_40; 
      break;
    default:
      std::cerr << "Unable to retrieve npv corrections for electron with radius = " << radius << "." << std::endl
                << "--- Radii must be one of {.15, .20, .25, .30, .35, .40} OR {15, 20, 25, 30, 35, 40}." << std::endl;
      return 0.;
  }
  
  int eta_bin_coarse = GetEtaBinCoarse(eta);
  
  float correction = 0.;
  if (npv_corrections_ptr && (eta_bin_coarse >= 0)) correction = npv_corrections_ptr[eta_bin_coarse]*float(nPV)*GeV;
  
  return correction;
}
//-----------------------------------------------------------------------


//-----------------------------------------------------------------------
// Internal function
// Returns error on correction based on number of vertices
float CaloIsoCorrection::GetNPVCorrectionError(float eta, float radius, unsigned int nPV, bool is_mc, ParticleType parttype){
  
  int newrad = GetRadius(radius);
  const float* npv_corrections_err_ptr(0);
  switch(newrad){
    case 15: 
      break;
    case 20: 
      npv_corrections_err_ptr = (float*)npv_corrections_relative_error_20; 
      break;
    case 25: 
      break;
    case 30: 
      npv_corrections_err_ptr = (float*)npv_corrections_relative_error_30; 
      break;
    case 35: 
      break;
    case 40: 
      npv_corrections_err_ptr = (float*)npv_corrections_relative_error_40; 
      break;
    default:
      std::cerr << "Unable to retrieve npv correction errors for radius = " << radius << "." << std::endl
                << "--- Radii must be one of {.15, .20, .25, .30, .35, .40} OR {15, 20, 25, 30, 35, 40}." << std::endl;
      return 0.;
  }
  
  int eta_bin_coarse = GetEtaBinCoarse(eta);
  
  float error = 0.;
  if (npv_corrections_err_ptr && (eta_bin_coarse >= 0)) error = npv_corrections_err_ptr[eta_bin_coarse]*GetNPVCorrection(eta,radius,nPV,is_mc,parttype);
  
  return error;
}
//-----------------------------------------------------------------------


//-----------------------------------------------------------------------
// Internal function
// Returns an absolute correction based on Energy Density for cone size 40
float CaloIsoCorrection::GetEDCorrection (float Etcone40, float Etcone40_ED_corrected, float radius){
  int newrad = GetRadius(radius);
  float floatrad = float(newrad)/100.;
  
  // energy density in a cone of 0.4 (minus the core!)
  float ED40 = Etcone40 - Etcone40_ED_corrected;
  if (newrad == 40) return ED40;
  const int neta = 5, nphi = 7;
  const float deta = 0.0125*neta*2;
  const float dphi = M_PI/256.*nphi*2;
  float area40 = M_PI * pow(0.4,2) - (deta * dphi);
  float areanew = M_PI * pow(floatrad,2) - (deta * dphi);
  // use the ratio of areas to calculate the energy density in new cone size
  float EDnew = ED40 * (areanew/area40);  
  return EDnew;
}
//-----------------------------------------------------------------------



