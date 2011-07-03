#! /usr/bin/env python

from math import tanh, pi
twopi = 2*pi

from minty.base import AnalysisBase
from minty.histograms import double_bins, mirror_bins, scale_bins
from minty.main import make_main
from minty.treedefs.egamma import Photon, Electron
from minty.utils import delta_r

PHIBINS = 100, -pi, pi
def plot_kinematics(ana, name, obj):
    hget = ana.h.get

    hget(name, "E",            b=[ana.ptbins],       t=";E [MeV]"       )(obj.E)
    
    hget(name, "pt",           b=[ana.ptbins],       t=";p_{T} [MeV]"   )(obj.pt)
    hget(name, "pt_many",      b=[(500,  0, 200e3)], t=";p_{T} [MeV]"   )(obj.pt)
    hget(name, "pt_many_wide", b=[(2500, 0,   1e6)], t=";p_{T} [MeV]"   )(obj.pt)
    
    hget(name, "eta",          b=[ana.etabins],      t=";#eta"          )(obj.eta)
    hget(name, "eta_many",     b=[ana.etabins_many], t=";#eta"          )(obj.eta)
    
    
    hget(name, "phi",          b=[PHIBINS],          t=";#phi"          )(obj.phi)
    hget(name, "eta_vs_phi",   b=[ana.etabins_many, PHIBINS], t=";#eta;#phi" )(obj.eta, obj.phi)
    
    #if getattr(obj, "conv", None) and getattr(obj, "isConv", None):
        #hget(name, "Rconv",    b=[(2000, 0, 1000)],   t="Conversion Radius;R_{conversion} [mm]")(obj.conv.R)

def plot_boson(ana, name, ph1, ph2):
    comb = ph1 + ph2
    
    H = ana.h.get
    
    m, pt = comb.m/1000, comb.pt/1000
    
    H(name, "boson/mass",           b=[(1000, 0, 500)],         t="Boson Mass;M_{#gamma#gamma} [GeV]")(m)
    H(name, "boson/mass_wide",      b=[(4000, 0, 2000)],        t="Boson Mass;M_{#gamma#gamma} [GeV]")(pt)
    H(name, "boson/pt",             b=[(1000, 0, 2000)],        t="Boson p_{T};p_{T}_{#gamma#gamma} [GeV]")(pt)
    
    H(name, "boson/pt_vs_mass", b=[(100, 0, 100), (100, 0, 250)], t="Boson p_{T} vs mass;p_{T}_{#gamma#gamma} [GeV];M_{#gamma#gamma} [GeV]")(pt, m)
    H(name, "boson/pt_vs_dphi", b=[(100, 0, 100), (20, 0, 6.2) ], t="Boson p_{T} vs dphi;p_{T}_{#gamma#gamma} [GeV];#Delta #phi")(pt, abs(ph1.phi - ph2.phi))
    H(name, "boson/mass_vs_dphi", b=[(100, 0, 250), (20, 0, 6.2) ], t="Boson Mass vs dphi;M_{#gamma#gamma} [GeV];#Delta #phi")(m, abs(ph1.phi - ph2.phi))
    #H(name, "boson/eta",            b=[(100, -8, 8)],           t="Boson #eta;#eta_{#gamma#gamma}")(comb.eta)
    #H(name, "boson/phi",            b=[(100, -pi, pi)],         t="Boson #phi;#phi_{#gamma#gamma}")(comb.phi)
    #H(name, "boson/deltar",         b=[(100, 0, twopi)],        t="Boson #Delta r;#Delta r_{#gamma#gamma}")(delta_r(ph1, ph2))
    #H(name, "boson/deltaphi",       b=[(200, 0, twopi)],        t="Boson #Delta #phi;#Delta #phi_{#gamma#gamma}")(abs(ph1.phi - ph2.phi))
    #H(name, "boson/deltaeta",       b=[(100, -8, 8)],           t="Boson #Delta #eta;#Delta #eta_{#gamma#gamma}")(ph1.eta - ph2.eta)
    #H(name, "boson/costhetastar",   b=[(100, -1, 1)],           t="Boson cos(#theta^{*});cos(#theta^{*})_{#gamma#gamma}")(tanh((ph1.eta - ph2.eta) / 2))
    #H(name, "boson/boost",          b=[(100, -1, 1)],           t="Boson Boost;#beta_{Z}_{#gamma#gamma}")(tanh((ph1.eta + ph2.eta) / 2))

def plot_boson_wconv(ana, name, ph1, ph2):
    plot_boson(ana, name, ph1, ph2)
    return
    if ph1.isConv and ph2.isConv:
        plot_boson(ana, (name, "convboth"), ph1, ph2)
    elif ph1.isConv and not ph2.isConv:
        plot_boson(ana, (name, "conv1"), ph1, ph2)
    elif ph2.isConv and not ph1.isConv:
        plot_boson(ana, (name, "conv2"), ph1, ph2)
    else:
        plot_boson(ana, (name, "convneither"), ph1, ph2)

def pass_event(counts, ana, event):
    # Total
    counts(PH_TOTAL)
        
    # Pass Trigger
    if ana.project == "data10":
        # 2010 requirements:
        # The above cut (event.RunNumber < 160889) also catches MC.
        if event.RunNumber < 160889:
            trigger = any(ph.L1_e >= 14000 for ph in event.photons)
        else:
            trigger = event.EF._2g15_loose
            
    elif ana.project == "data11":
        trigger = event.EF._2g20_loose
    
    if not trigger: return
    counts(PH_2G20L)

    if not event.is_grl: return
    counts(PH_GRL)
    
    # Requirement for other paper: and v.z < 150. 
    if not any(v.nTracks >= 3 for v in event.vertices): return
    counts(PH_VTX)
    
    return True

def photon_selection(ana, event, counts, pt_cut):
    
    good_photons = event.photons
    
    if len(good_photons) < 2: return
    counts(PH_N)
    
    # fiducal is abs(self.etas2) < 1.37 or 1.52 < abs(self.etas2) < 2.37
    good_photons = [ph for ph in good_photons if ph.pass_fiducial_eta]
    if len(good_photons) < 2: return
    counts(PH_ETA)
    
    # pt_via_clE_etas2 == ph.cl.E / cosh(ph.etas2)
    good_photons = [ph for ph in good_photons if ph.pt_via_clE_etas2 >= pt_cut]
    if len(good_photons) < 2: return
    counts(PH_PT)
    
    good_photons = [ph for ph in good_photons if ph.my_oq]
    if len(good_photons) < 2: return
    counts(PH_OQ)

    good_photons = [ph for ph in good_photons if ph.loose]
    if len(good_photons) < 2: return
    counts(PH_LOOSE)

    return sorted(good_photons, key=lambda o: o.pt, reverse=True)

PT_CUTS = 25000, 27500, 30000

PHOTON_CUTFLOW = (
    "named", "total", "2g20_loose", "grl",  "vertex", "nphot", "eta", "pt", 
    "oq", "loose",   "tight",  "tightar",  "larError",  "jetcleaning")
(            PH_TOTAL, PH_2G20L,    PH_GRL, PH_VTX,   PH_N,    PH_ETA, PH_PT, 
    PH_OQ, PH_LOOSE, PH_TIGHT, PH_TIGHTAR, PH_LARERROR, PH_JETCLEANING) = range(len(PHOTON_CUTFLOW)-1)

def plot_photons(ana, event, name, counts, good_photons, 
                 check_jet_lar=False, dphi_cut=False, plotbulk=False):
        
    ph1, ph2 = good_photons[:2]
    
    # my_tight is robust_tight for data10, and "tight" for data11
    #if not (ph1.my_tight and ph2.my_tight):
        #return
        
    counts(PH_TIGHT)
    
    #ph1C = ph1.v16_corrections()
    #ph2C = ph2.v16_corrections()
    
    # Loose plots with corrections
    #plot_kinematics (ana, (name, "corrected/ph/1"), ph1C)
    #plot_kinematics (ana, (name, "corrected/ph/2"), ph2C)
    plot_boson_wconv(ana, (name, "corrected/ph"), ph1, ph2) #C, ph2C)
    

def multi_pt_cutflow(ana, event):
    counters = []
    for pt in PT_CUTS:
        gev = pt / 1000
        c = ana.h.get("photon_cutflow_{0}GeV".format(gev), b=[PHOTON_CUTFLOW])
        counters.append(c)
    
    def fill_all(i):
        for x in counters: x(i)
    
    if not pass_event(fill_all, ana, event):
        return
    
    def dummycounter(i): pass
    
    for pt, counts in zip(PT_CUTS, counters):
        photons = photon_selection(ana, event, counts, pt)
        if not photons:
            continue
        
        ptstr = "{0}GeV".format(pt/1000)
        
        plot_photons(ana, event, ptstr,              counts,       photons, plotbulk=True)
        

class PtBumpAnalysis(AnalysisBase):
    def __init__(self, tree, options):
    
        super(PtBumpAnalysis, self).__init__(tree, options)
        
        self.ptbins = ("var", 15, 20, 25, 30, 35, 40, 50, 60, 100, 140, 180, 
                       220, 300, 380, 460, 620, 1000)
        self.ptbins = scale_bins(self.ptbins, 1000)
        
        self.ptbins_wide = "var", 15, 45, 60, 80, 120, 200, 400, 1000
        self.ptbins_wide = scale_bins(self.ptbins_wide, 1000)
        
        self.etabins_sym = "var", 0., 0.60, 1.37, 1.52, 1.81, 2.37
        self.etabins = mirror_bins(self.etabins_sym)
        self.etabins_many = double_bins(self.etabins, 3)
        
        # Tasks to run in order
        self.tasks.extend([
            multi_pt_cutflow,
        ])

ptbumpana_main = make_main(PtBumpAnalysis)
if __name__ == "__main__":
    ptbumpana_main()
