//#include "EnergyRescaler.h"
#include <iostream>

#include <vector>
void plot_sys()
{
  
  
  //  gROOT->ProcessLine(".L Macros/Sys.C");
  
  gROOT->ProcessLine(".L EnergyRescaler.cxx+");
  
    
  //gStyle->SetOptFit(1111);
  EnergyRescaler  eRescale;
  eRescale.useDefaultCalibConstants();
  
  string ptype="ELECTRON";
  ptype="UNCONVERTED_PHOTON";
  
  double cl_eta=0.7, cl_et=20;
  double er_up,er_do;

  
  int color1=kMagenta+2;
  int color2=kMagenta;
  if(ptype!="ELECTRON")
    {
      color1=kAzure;
      color2=kAzure+10;
    }


  
  const int Neta=7;
  double etas[Neta]={0,0.6,1.1,1.7,2.1,3.,4.};
  
  for(int ieta=0; ieta<Neta; ieta++)
  {
    const int N=1000;
    double x[2*N+1];
    double y[2*N+1];
    double y_nomat[2*N+1];
    double yES[2*N+1];
    double yES_nomat[2*N+1];
    double etmin=10;
    double etmax=1000;
    double step=(etmax-etmin)/(N-1);
    double cl_eta=etas[ieta];
    for(int i=0;i<N;i++)
      {

	x[i]=etmin+i*step;
	eRescale.getError(cl_eta,x[i], er_up, er_do,ptype);
	y[i]=er_up;
	eRescale.getError(cl_eta,x[i], er_up, er_do,ptype,false);
	y_nomat[i] = er_up;

	x[N+i]=etmax-i*step;
	eRescale.getError(cl_eta,x[N+i], er_up, er_do,ptype);
	y[N+i]=er_do;
	eRescale.getError(cl_eta,x[N+i], er_up, er_do,ptype,false);
	y_nomat[N+i] = er_do;



	//	cout<<i<<"  "<<x[i]<<"  "<<y[i]<<"  "<<x[N+i]<<"  "<<y[N+i]<<endl;

      }
    x[2*N]=x[0];  y[2*N]=y[0];
    y_nomat[2*N]=y_nomat[0];

    TCanvas*canvas = new TCanvas("canvas","canvas",800*2,600*2);
    //    canvas->SetLineWidth(3);
    //    canvas->SetGrid();
    canvas->SetLogx();

    TGraph* TG_er = new TGraph(2*N+1,x,y);
    TG_er->GetXaxis()->SetTitle("E_{T} (GeV)");
    TG_er->GetYaxis()->SetTitle("Energy scale uncertainties");

    TG_er->GetXaxis()->SetMoreLogLabels();
    TG_er->SetLineWidth(3);
    TG_er->SetLineColor(1);
    TG_er->Draw("AFL");
    TG_er->SetFillColor(color1);
    //    TG_er->SetFillStyle(3001);
    TG_er->SetMaximum(0.04);
    TG_er->SetMinimum(-0.04);

    TGraph* TG_nomat_er = new TGraph(2*N+1,x,y_nomat);
    TG_nomat_er->GetXaxis()->SetMoreLogLabels();
    TG_nomat_er->SetLineWidth(0);
    TG_nomat_er->SetLineStyle(1);
    TG_nomat_er->SetLineColor(color2);
    TG_nomat_er->Draw("F");
    //TG_nomat_er->Draw("L");
    TG_nomat_er->SetFillColor(color2);
    //    TG_nomat_er->SetFillStyle(3001);
    TG_er->Draw("L");

  
    TLegend* legend = new TLegend(0.2,0.8,0.85,0.94);
    legend->SetBorderSize(0);
    legend->SetTextSize(0.04);
    legend->SetFillStyle(0);
    legend->SetFillColor(0);
    legend->SetTextFont(42);
    legend->AddEntry(TG_er,"Total","f");
    legend->AddEntry(TG_nomat_er,"Total except material","F");
    legend->Draw();
    
    TString text;
    if(ieta==0) text="0<|#eta|<0.6";
    if(ieta==1) text="0.6<|#eta|<1.0";
    if(ieta==2) text="1.0<|#eta|<1.37";
    if(ieta==3) text="1.52<|#eta|<1.8";
    if(ieta==4) text="1.8<|#eta|<2.5";
    if(ieta==5) text="2.5<|#eta|<3.2";
    if(ieta==6) text="3.2<|#eta|<4.9";

    TLatex* etalatex = new TLatex(0.5,0.2, text);
    etalatex->SetNDC();
    etalatex->SetTextSize(0.05);
    etalatex->SetTextFont(42);
    etalatex->Draw();

    TString ptypetext;
    if(ptype=="ELECTRON")
      ptypetext="Electron";
    else
      ptypetext="Photon";

    TLatex* ptypelatex = new TLatex(0.5,0.28, ptypetext);
    ptypelatex->SetNDC();
    ptypelatex->SetTextSize(0.05);
    ptypelatex->SetTextFont(42);
    ptypelatex->Draw();




//     TGraph* TG_er_up_nomat = new TGraph(N,x,yup_nomat);
//     TG_er_up_nomat->SetLineWidth(3);
//     TG_er_up_nomat->SetLineColor(3);
//     TG_er_up_nomat->Draw("L");
//     TG_er_up_nomat->SetMaximum(0.02);
//     TG_er_up_nomat->SetMinimum(-0.02);
    
//     TGraph* TG_er_do_nomat = new TGraph(N,x,ydo_nomat);
//     TG_er_do_nomat->Draw("L");
//     TG_er_do_nomat->SetLineWidth(3);
//     TG_er_do_nomat->SetLineColor(3);

    char tmp[100];

    if (ptype=="ELECTRON")
    {  
     sprintf(tmp,"%s%d%s","sys_elec_",ieta,".eps");
    }
  else
    {  
     sprintf(tmp,"%s%d%s","sys_pho_",ieta,".eps");
    }
     canvas->Print(tmp);
    
  }

}

