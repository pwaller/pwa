
#include "EnergyRescaler.h"

#include <vector>
#include <iostream>
#include <fstream>

#include <string>
#include <cstdlib>
#include <iomanip>
#include <cmath>
#include <cctype>


using namespace std;


///default constructor
EnergyRescaler::EnergyRescaler()
{

   //default seed
   SetRandomSeed();
  
}


//destructor
EnergyRescaler::~EnergyRescaler()
{


}

void EnergyRescaler::SetRandomSeed( unsigned seed){

   m_random3.SetSeed(seed);

}

  
bool EnergyRescaler::readCalibConstants(std::string fname)
{ 

   
   if( corrVec.size()) {
      std::cout<<" WARNING having already  "<<corrVec.size()<<"  corrections "<<std::endl;
      corrVec.clear();

   }

   
   std::ifstream infile; 
  
   infile.open(fname.c_str()); 


   if(!infile.good()) 
   { 
      cout<<"CANT OPEN CUT FILE " << fname <<" GOING TO EXIT"<<endl; 
      exit(1); 
   }     
   
   std::cout<<"READING FILE  "<< fname<<std::endl;

   calibMap myMap;


   while( !infile.eof() )
   {

      double eta=-10.,etaErr=-10.,  phi=-10., phiErr=-10., alpha=-100., err=-100.;

     

      infile >>eta>>etaErr>>phi>> phiErr>>alpha>>err;
      if( !infile.good()  ) break; 

      myMap.eta= eta;
      myMap.etaBinSize =etaErr;
      myMap.phi = phi;
      myMap.phiBinSize = phiErr;
      myMap.alpha = alpha;
      myMap.alphaErr = err;
     
      corrVec.push_back(myMap);


   }
  


   return true; 
} 
 

double EnergyRescaler::applyEnergyCorrection(double eta, double phi, double energy, double et,  int value, std::string ptype)
{ 
 
   ////no correction for 2011 data yet
   //if(corr_version!="2010")return energy;

   double corrEnergy=-999.0;
   
   if(corrVec.size()==0)
   {
      std::cout<<"NO CORRECTIONS EXISTS, PLEASE EITHER SUPPLY A CORRECTION FILE OR USE THE DEFAULT CORRECTIONS"<<std::endl;
   }

   for (unsigned int i=0; i< corrVec.size(); i++)
   {

      if( 
         eta>=( corrVec.at(i).eta - corrVec.at(i).etaBinSize/2.) && eta< ( corrVec.at(i).eta+corrVec.at(i).etaBinSize/2.)  &&
         phi>=( corrVec.at(i).phi - corrVec.at(i).phiBinSize/2.) && phi< ( corrVec.at(i).phi+corrVec.at(i).phiBinSize/2.) 
         ) 
      { 

         
        
         for(std::string::iterator p = ptype.begin(); ptype.end() != p; ++p)
         *p = toupper(*p);


         double er_up=-99,er_do=0; 
         double scale=0.;


         switch (value)
         {
            default:
            {
               scale=corrVec.at(i).alpha;
               break;
            }
            case NOMINAL:
            {
               scale=corrVec.at(i).alpha;
             
               break;
            }
            case ERR_UP:
            {
               scale=corrVec.at(i).alpha;
               getError(eta,et, er_up, er_do, ptype);
               scale+=er_do;
             
               break;
            }
            case ERR_DOWN:
            {
               scale=corrVec.at(i).alpha;
               getError(eta,et, er_up, er_do, ptype);
               scale+=er_up;
            
               break;
            }
         }

        

         corrEnergy =  energy/(1.+ scale);

         // std::cout<<" eta : "<<eta <<" uncorrected energy : "<<    energy <<" corr energy : "<< corrEnergy<<" scale : "<< corrVec.at(i).alpha <<endl;
         break;
      }
   }

   if( corrEnergy==-999.)return energy;
   else return corrEnergy;

} 



double EnergyRescaler::getSmearingCorrection(double eta, double energy, int value, bool mc_withCT, std::string corr_version)
{
  //=====================================
  //bins definition:
  //=====================================
  static const int nbins=6;
  static double boundaries[nbins+1]={0,0.6,1.37,1.52,2.47,3.2,4.9};
  
  //===================================== 
  //default MC parameters
  //=====================================
  static  double Smc[nbins]={0.10,0.15,0.20,0.15,0.30,0.30};
  static  double Smc_er=0.;
  static  double Cmc=0.007;

  //=====================================
  //constant term measured in data 
  //=====================================
  //2010 
  static  double Cdata_nominal[nbins]={0.};
  static  double Cdata_erup[nbins]={0.};
  static  double Cdata_erdo[nbins]={0.};

  static double Cdata_nominal_2011[nbins]={0.011,0.011,0.018,0.018,0.06,0.02};  
  static double Cdata_erup_2011[nbins]={0.005,0.005,0.006,0.006,0.02,0.02};  
  static double Cdata_erdo_2011[nbins]={0.006,0.006,0.006,0.006,0.02,0.024}; 
  
  static double Cdata_nominal_2010[nbins]={0.011,0.011,0.018,0.018,0.04,0.02};
  static double Cdata_erup_2010[nbins]={0.005,0.005,0.006,0.006,0.011,0.010};
  static double Cdata_erdo_2010[nbins]={0.006,0.006,0.006,0.006,0.011,0.016}; 

  
  if(corr_version!="2010"){
 
     for(int i=0; i<nbins; i++){
        Cdata_nominal[i]= Cdata_nominal_2011[i];
        Cdata_erup[i]=Cdata_erup_2011[i];
        Cdata_erdo[i]=Cdata_erdo_2011[i];
     }


  }else{
     for(int i=0; i<nbins; i++){
     Cdata_nominal[i]= Cdata_nominal_2010[i];
     Cdata_erup[i]= Cdata_erup_2010[i];
     Cdata_erdo[i]= Cdata_erdo_2010[i];
     }
  }

 
//  for(int i=0;i<nbins;i++)cout<<"nom : "<< Cdata_nominal[i]<<"  "<<Cdata_erup[i]<<"  "<< Cdata_erdo[i]<<endl;

  //=====================================
  //compute Cdata +/- error  and select the eta bin
  //=====================================
  double Cdata_do[nbins];
  double Cdata_up[nbins];
  int bin =-1;
  for(int i=0;i<nbins;i++)
    {
      if(fabs(eta)>boundaries[i] && fabs(eta)<boundaries[i+1])
	{
	  bin=i;
	}
      Cdata_do[i]=Cdata_nominal[i]-Cdata_erdo[i];
      Cdata_up[i]=Cdata_nominal[i]+Cdata_erup[i];
    }

  //=====================================
  //choose which value to use
  //=====================================
  double* Cdata;
  switch (value)
    {
    default:
      {
	Cdata=Cdata_nominal;
	break;
      }
    case NOMINAL:
      {
	Cdata=Cdata_nominal;
	break;
      }
    case ERR_UP:
      {
	Cdata=Cdata_up;
	break;
      }
    case ERR_DOWN:
      {
	Cdata=Cdata_do;
	break;
      }
    }

  //=====================================
  //Smearing procedure
  //=====================================

  double sigma2 = std::pow(Cdata[bin]*energy,2) + std::pow(Smc[bin]*(1+Smc_er)*std::sqrt(energy),2) - std::pow(Smc[bin]*std::sqrt(energy),2);  
  if (mc_withCT==true) sigma2= sigma2-std::pow(Cmc*energy,2);
  
  //Smearing procedure for Ashfaq
  //  Smc_er=0.2;
  //sigma2=std::pow(Smc[bin]*(1+Smc_er)*std::sqrt(energy),2) - std::pow(Smc[bin]*std::sqrt(energy),2);

  if(sigma2<=0) return 1;
  
  double sigma = sqrt(sigma2);
  //double DeltaE0 = gRandom->Gaus(0,sigma);
  double DeltaE0 = m_random3.Gaus(0,sigma);

  double cor0=(energy+DeltaE0)/energy;
  
  return cor0;
  
}


void EnergyRescaler::getError(double cl_eta,double cl_et, double &er_up, double &er_do, std::string ptype,bool withXMAT,bool withPS)
{
  // Quick and dirty
  // Need to optimized

  er_up=-1;
  er_do=-1;

  static const int nbins=8;
  static double boundaries[nbins+1]={0,0.6,1.00,1.37,1.52,1.8,2.47,3.2,4.9};

  //systematics 
  static double stat[nbins]               ={0.0010, 0.0020, 0.0020, 777, 0.0020, 0.0020, 0.005, 0.01};
  static double sys_mcclosure[nbins]      ={0.0010, 0.0010, 0.0010, 777, 0.0010, 0.0010, 0.002, 0.002};
  static double sys_comparison[nbins]     ={0.0010, 0.0010, 0.0010, 777, 0.0010, 0.0010, 0.01, 0.008}; 
  static double sys_pileup[nbins]         ={0.0010, 0.0010, 0.0010, 777, 0.0010, 0.0010, 0.001, 0.001}; //check forward? 
  static double sys_medium2tight_up[nbins]={0.0010, 0.0010, 0.0010, 777, 0.0020, 0.0020, 0,0};
  static double sys_loose2tight_forward[nbins]    ={0.0000, 0.0000, 0.0000, 777, 0.0000, 0.0000, 0.012, 0.01};

  static double sys_masscut[nbins]        ={0.0010, 0.0010, 0.0010, 777, 0.0020, 0.0020, 0.002, 0.006};
  static double sys_elecLin[nbins]        ={0.0010, 0.0010, 0.0010, 777, 0.0010, 0.0010, 0.001, 0.001};//forward?
  static double sys_xtalkE1[nbins]        ={0.0010, 0.0010, 0.0010, 777, 0.0010, 0.0010, 0.001, 0.001};//forward?
  static double sys_lowpt  [nbins]        ={0.0100, 0.0100, 0.0100, 777, 0.0100, 0.0100, 0.01,  0.01};
  static double sys_HV     [nbins]        ={0.0000, 0.0000, 0.0000, 777, 0.0000, 0.0000, 0.006, 0.008};

  static double PS_B[nbins]={-0.00025312, -0.0011569, -0.00211677, 777, -0.00175762*2, 000, 000, 000};
//  static double PS_A[nbins]={ 0.00187341, 0.00840421,  0.016034  , 777,   0.0127718*2, 000, 000, 000};

  //Material electron
 
  static double elec_XMAT_a[nbins] = {-0.0083,  -0.013,	-0.025,	777, -0.023, -0.019, -0.042, -0.014  };
  static double elec_XMAT_b[nbins] = {-0.055, -0.019, -0.014, 777, -0.026, -0.019, -0.041, -0.016};
  static double elec_XMAT_MAX[nbins]={  0.003,  0.008,  0.015,  777,   0.010,   0.01  ,0.01, 0.01};  

 //Material photon
  static double pho_XMAT_MAX[nbins]={  0.003,  0.005,  0.010,  777,   0.010,   0.01  ,0, 0.} ;
 static double pho_PS_shift[nbins] ={  0.001,  0.002,  0.003,  777,   0.002*2,   0.000  ,0, 0.} ;

  int bin =-1;
  for(int i=0;i<nbins;i++)
    {
      if(fabs(cl_eta)>=boundaries[i] && fabs(cl_eta)<boundaries[i+1])
	{
	  bin=i;
	  break;
	}
    }
  if(bin==-1) return;

  //==================================
  //crack region
  //==================================
  if(bin==3)
    { 
      er_up=0.05;
      er_do=-0.05;
      return;
    }

  //==================================
  //PS
  //==================================
  double PS_up=0,PS_do=0;
  
  if(withPS==true)
    {          
      if(abs(cl_eta)<1.8)
	{
	  double shift=0;
	  if(ptype=="UNCONVERTED_PHOTON" || ptype =="CONVERTED_PHOTON")
	    {
	  shift=pho_PS_shift[bin];
	    }
	  double PS=PS_B[bin]*(log(cl_et)-log(40))-shift;
	  if(PS>=0)
	    {
	      PS_up=PS;
	      PS_do=-PS;
	    }
	  else
	    {
	      PS_up=-PS;
	      PS_do=PS;
	    }
	}
      
    }
  

  //==================================
  //material
  //==================================
  double XMat_up = 0;
  double XMat_do = 0;
  
  if(withXMAT==true)
    {
      
      if(ptype=="ELECTRON")
	{
	  double xmat= 0;

	  //	  cout<<elec_XMAT_a[bin]<<" "<<elec_XMAT_b[bin] <<endl;
	  xmat= elec_XMAT_a[bin]*exp(cl_et* elec_XMAT_b[bin])+elec_XMAT_MAX[bin];
	  //alpha = a * exp(Pt * b) + c
	  
	  if(xmat>0)
	    {
	      XMat_up=xmat;
	    }
	  else  XMat_do=xmat;

// 	  if(XMat_up>elec_XMAT_MAX[bin])
// 	    XMat_up=elec_XMAT_MAX[bin];	
	  
	}



      
      else if(ptype=="UNCONVERTED_PHOTON" || ptype =="CONVERTED_PHOTON")
	//else if(ptype=="PHOTON")
	{      
	  XMat_up=pho_XMAT_MAX[bin];
	  XMat_do=0;
	  //      cout<<XMat_up<<endl;
	}                 
    }
  //==================================
  //lowpt
  //==================================
  double lowpt=0;
  if(cl_et<20)
    {
      lowpt =sys_lowpt[bin]/(10-20)*(cl_et-20);
    }

  er_up= sqrt(stat[bin]*stat[bin]+
 	      sys_mcclosure[bin]*sys_mcclosure[bin]+
 	      sys_comparison[bin]*sys_comparison[bin]+
 	      sys_pileup[bin]*sys_pileup[bin]+
  	      sys_medium2tight_up[bin]*sys_medium2tight_up[bin]+
	      sys_loose2tight_forward[bin]*sys_loose2tight_forward[bin]+
  	      sys_masscut[bin]*sys_masscut[bin]+
  	      sys_HV[bin]*sys_HV[bin]+
  	      sys_elecLin[bin]*sys_elecLin[bin]+
	      sys_xtalkE1[bin]*sys_xtalkE1[bin]+
 	      PS_up*PS_up+
 	      XMat_up*XMat_up+
	      lowpt*lowpt);
  
  er_do= -sqrt(stat[bin]*stat[bin]+
	       sys_mcclosure[bin]*sys_mcclosure[bin]+
	       sys_comparison[bin]*sys_comparison[bin]+
	       sys_pileup[bin]*sys_pileup[bin]+
	       sys_loose2tight_forward[bin]*sys_loose2tight_forward[bin]+
	       sys_masscut[bin]*sys_masscut[bin]+
	       sys_HV[bin]*sys_HV[bin]+
	       sys_elecLin[bin]*sys_elecLin[bin]+
	       sys_xtalkE1[bin]*sys_xtalkE1[bin]+
	       PS_do*PS_do+
	       XMat_do*XMat_do+
	       lowpt*lowpt);
  //   er_up=XMat_up;
  //   er_do=XMat_do;
  
  return;
}





/////default constants, for 60 eta bins
bool  EnergyRescaler::useDefaultCalibConstants( std::string corr_vers)
{
   
   corr_version=corr_vers;

   //if(corr_version!="2010")return true;

   const int netaBins=58;
   const int nphiBins=58;
   
   ///for 2011
   const int netaBinsFor2011=32;
   const int nphiBinsFor2011=32;
   
  
   double m_2pi = 2.*acos(-1.); 
   //cout<<" pi : "<<acos(-1.)<<"  M_PI : "<<M_PI<<" 2pi : "<<m_2pi<<endl;
   

  

   if( corrVec.size()) {
      std::cout<<" WARNING having already  "<<corrVec.size()<<"  corrections "<<std::endl;
      corrVec.clear();

   }
   

   

  
   double eta_tmp[netaBins]={   
      -4.45, -3.60, -3.00, -2.65, -2.435, -2.35, -2.25, -2.15, -2.05, -1.95, -1.85,	-1.75,	-1.65,
      -1.56, -1.445,	-1.335,	-1.25, -1.15,	-1.05,	-0.95,	-0.85,	-0.75,	-0.65,	-0.55,	-0.45,	-0.35,
      -0.25, -0.15,	-0.05,	0.05,  0.15,	0.25,	0.35,	0.45,	0.55,	0.65,	0.75,	0.85,	0.95,
       1.05, 1.15,	1.25,	1.335, 1.445,	1.56,	1.65,	1.75,	1.85,	1.95,	2.05,	2.15,	2.25,
       2.35,	2.435,   2.65,	3.00,	3.60,	4.45
         };
   

   


    double etaBinWidth_tmp[netaBins]= {
       0.9, 0.8, 0.4, 0.3, 0.07,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.08,	0.15,	0.07,	0.1,	0.1,	0.1,	        0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	        0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.1,	0.07,	0.15,	0.08,	0.1,	0.1,	0.1,	0.1,	        0.1,	0.1,	0.1,	0.1,	0.07,    0.3,	0.4,	0.8,	0.9 };

   
    

   
    double phi_tmp[nphiBins]={
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 	0, 0, 0, 0, 0, 0, 0, 0,	0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0,	0, 0 };

    double phiBinWidth_tmp[nphiBins]={
       m_2pi, m_2pi, m_2pi, m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,
       m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi, m_2pi,m_2pi,m_2pi,m_2pi,
       m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi, m_2pi,
       m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,
       m_2pi,m_2pi, m_2pi,m_2pi,m_2pi,m_2pi,m_2pi, m_2pi, m_2pi, m_2pi, m_2pi, m_2pi };


    
    double alpha_tmp[netaBins]= {
    0.046962, 0.044332,	-0.007777,-0.045341, -0.053683,-0.005040,0.003357,0.003830,0.016857,0.012810,
    0.008882,-0.016864,-0.021280,-0.011215,-0.008958,-0.010248, 0.005199,0.007815,-0.000701,0.003837,0.003222,
    -0.004017,-0.005908,-0.009560,-0.005382,-0.012158,-0.005060,-0.008274, -0.006701,-0.002734,-0.012920, 
    -0.010972,-0.006823,-0.007234,-0.002612,-0.004301,0.001580,-0.001986,-0.001306,0.005748, 0.002906, 
    0.001381,-0.001584,0.000799,-0.002511,-0.030902,-0.016416,-0.004976,0.002408,0.018706,-0.004309,-0.002673,
    -0.001735,-0.050173, -0.034703,	-0.003296,	0.047351,	0.028374
   };

   

   

   double alphaError_tmp[netaBins]={ 
      0.019646, 0.011500, 0.008761, 0.009514, 0.008341,0.006345,0.005522,0.005089,0.005387,0.005861,
      0.005821,0.005119,0.006227,0.009148,0.003920,0.004309,0.002929,  0.003882,0.004054,0.003716,0.003673,
      0.003832,0.003275,0.002075,0.004004,0.002497,0.003182,0.002512,0.003974,0.002302, 0.003670,0.003322,
      0.003978,0.002164,0.001984,0.002093,0.002372,0.003843,0.004138,0.004277,0.003003,0.004690,0.005480,
      0.006306,	0.007338,0.005939,0.004472,0.004535,0.005453,0.008538,0.004554,0.003382,0.005504,0.007577,
      0.010095,	0.009122,	0.013400,	0.02588
   };


   //////NUMBERS for 2011 data
   double etaFor2011_tmp[netaBinsFor2011]={ 
      -4.05,	-3.00,	-2.65,	-2.385,	-2.2,	-2.00,	-1.8,	-1.61,	-1.445,	-1.285,	-1.1,	-0.9,	-0.7,	-0.5,	-0.3,	-0.1,	0.1,	0.3,	0.5,	0.7,	0.9,	1.1,	1.285,	1.445,	1.61,	1.8,	2.0,	2.2,	2.385,	2.65,	3.0,	4.05
   };

    double etaBinWidthFor2011_tmp[netaBinsFor2011]= {
       1.7,	0.4,	0.3,  0.17,	0.2,	0.2,	0.2,	0.18,	0.15,	0.17,	0.2,	0.2,	0.2,	0.2,	0.2,	0.2,	0.2,	0.2,	0.2,	0.2,	0.2,	0.2,	0.17,	0.15,	0.18,	0.2,	0.2,	0.2,	0.17,   0.3,	0.4,	1.7
    };

    double phiFor2011_tmp[nphiBinsFor2011]={
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        };

    double phiBinWidthFor2011_tmp[nphiBinsFor2011]={
       m_2pi, m_2pi, m_2pi, m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,
       m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi, m_2pi, m_2pi, m_2pi, m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,
       m_2pi,m_2pi,m_2pi,m_2pi,m_2pi,m_2pi
       };


    
    double alphaFor2011_tmp[netaBinsFor2011]= {
       0.01767670,
       0.01193680,
       0.02863680,
       -0.00182836,
       0.00379822,
       0.00949851,
       0.00388223,
       -0.00630638,
       -0.01459190,
       0.00191748,
       0.00120518,
       -0.00116847,
       0.00316491,
       0.00534383,
       -0.00259050,
       -0.00303995,
       -0.00114055,
       -0.00152093,
       0.00346042,
       0.00316020,
       -6.51986e-05,
       0.00237845,
       0.00391017,
       -0.01056940,
       -0.01190480,
       -0.00177316,
       -0.00101658,
       -0.00430559,
       -0.01101630,
       0.01681920,
       0.01459770,
       0.00328200
       
    };
   

    double alphaErrorFor2011_tmp[netaBinsFor2011]={ 
      0.00365611,
      0.00269144,
      0.00253709,
      0.00124745,
      0.00094802,
      0.00094137,
      0.00097271,
      0.00130736,
      0.00170269,
      0.00091738,
      0.00076709,
      0.00072777,
      0.00067059,
      0.00063910,
      0.00064532,
      0.00063576,
      0.00066304,
      0.00064027,
      0.00066183,
      0.00068352,
      0.00075179,
      0.00080414,
      0.00093506,
      0.00167934,
      0.00131510,
      0.00097932,
      0.00095425,
      0.00097240,
      0.00127444,
      0.00258217,
      0.00265290,
      0.00360700

   };




    calibMap myMap;
    
    if(corr_version!="2010"){
       
       for(int i=0; i<netaBinsFor2011; i++){

          //for(int j=0; j<nphiBins; j++){///this should be a 2d array finally
          //}

          myMap.eta= etaFor2011_tmp[i];
          myMap.etaBinSize =etaBinWidthFor2011_tmp[i];
          myMap.alpha = alphaFor2011_tmp[i];
          myMap.phi = phiFor2011_tmp[i];
          myMap.phiBinSize = phiBinWidthFor2011_tmp[i];
          myMap.alphaErr = alphaErrorFor2011_tmp[i];

          corrVec.push_back(myMap);

       }
        

    }else{

       
       for(int i=0; i<netaBins; i++){

          //for(int j=0; j<nphiBins; j++){///this should be a 2d array finally
          //}

          myMap.eta= eta_tmp[i];
          myMap.etaBinSize =etaBinWidth_tmp[i];
          myMap.alpha = alpha_tmp[i];
          myMap.phi = phi_tmp[i];
          myMap.phiBinSize = phiBinWidth_tmp[i];
          myMap.alphaErr = alphaError_tmp[i];

          corrVec.push_back(myMap);

       }


    }//if-else


   return true;
}



bool EnergyRescaler::printMap()
{

   for (unsigned int i=0; i< corrVec.size(); i++)
   {
      std::cout<<"eta :  "<< corrVec.at(i).eta <<
         " etaErr : " <<corrVec.at(i).etaBinSize<<
         " phi    :  "<<corrVec.at(i).phi<<
         " phiErr :  "<<corrVec.at(i).phiBinSize<<
         " alpha  :  "<<corrVec.at(i).alpha<<
         " alphaErr : "<<corrVec.at(i).alphaErr<<endl;
   }


   return true;

}




