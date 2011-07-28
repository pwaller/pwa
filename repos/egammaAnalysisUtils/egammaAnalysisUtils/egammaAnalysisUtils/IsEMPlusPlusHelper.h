#ifndef ISEMPLUSPLUSHELPER_H
#define ISEMPLUSPLUSHELPER_H

/********************************************************************

    Name:     IsEMPlusPlusHelper.cxx
    Package:  offline/Reconstruction/egamma/egammaAnalysis/egammaAnalysisUtils

    Authors:  John Alison <john.alison@cern.ch>
              Chris Lester <clester@sas.upenn.edu>

    Created:  May 2011
    Comment:  Athena Wrapper for IsEMPlusPlusDefs.cxx 

    Includes:
  
     Medium++ Optimization for  > 20 GeV electrons (MC corrected from Z T and P)
     Medium++ Optimization for  > 20 GeV electrons (MC corrected from Z T and P)
	   Loose++  Optimization for  > 20 GeV electrons (MC corrected from Z T and P)
	   
     Tight++ Optimization for  > 20 GeV electrons (MC corrected from Tight Ele)
     Medium++ Optimization for 10-20 GeV electrons (MC corrected from Tight Ele )
	   Loose++ Optimization for 10-20 GeV electrons (MC corrected from Tight Ele )
	   
    Usage:
       The IsEMTightPlusPlus, IsMediumPlusPlus, and IsLoosePlusPlus methods take an egamma object
       and returns true if the electron satisfies the loose++ or medium++ requriements.
       It returns false otherwise.

     Additional output will be givedn if debug is set, (false by default).
     
     The trigger bit emulates the online selction of e20_medium1.

   Created:
      May 2011

*********************************************************************/
#include <iostream>
#include <fstream>
#include <string>
#include "egammaEvent/egamma.h"

namespace isEMPlusPlusHelper{

  bool IsLoosePlusPlus(const egamma* eg,
		       bool debug=false,
		       bool isTrigger=false);

  bool IsMediumPlusPlus(const egamma* eg, 
			bool debug=false,
			bool isTrigger=false);

  bool IsTightPlusPlus(const egamma* eg, 
			bool debug=false,
			bool isTrigger=false);
 
}

#endif //
