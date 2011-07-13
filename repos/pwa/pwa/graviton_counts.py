#! /usr/bin/env python

from math import tanh, pi
twopi = 2*pi

from minty.base import AnalysisBase
from minty.histograms import double_bins, mirror_bins, scale_bins, log_binning
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
    
    if getattr(obj, "conv", None) and getattr(obj, "isConv", None):
        hget(name, "Rconv",    b=[(2000, 0, 1000)],   t="Conversion Radius;R_{conversion} [mm]")(obj.conv.R)
    
    if ana.mc:
        if "truth" in name or not hasattr(obj, "truth"): return
        namet = name, "truth"
        objt = obj.truth
        plot_kinematics(ana, namet, objt)

def plot_shower(ana, name, obj):
    hget = ana.h.get
    
    B = [ana.ptbins_wide, ana.etabins_sym]
    V = obj.cl.pt, abs(obj.etas2)
    T = ";p_{T} (cluster) [MeV];#eta_{s2}"
    
    hget(name, "et",        b=[ana.ptbins], t=";E_{T} [MeV]"          )(obj.et)
    hget(name, "cl_pt",     b=[ana.ptbins], t=";p_{T} (cluster) [MeV]")(obj.cl.pt)
    hget(name, "cl_pt_many",     b=[(500, 0, 200e3)], t=";p_{T} (cluster) [MeV]")(obj.cl.pt)
    
    hget(name, "etas2",     b=[ana.etabins], t=";#eta_{s2}"           )(obj.etas2)
    hget(name, "etas2_many",     b=[ana.etabins_many], t=";#eta_{s2}"           )(obj.etas2)
    
    hget(name, "clpt_vs_etas2", b=[ana.ptbins, ana.etabins], t=";p_{T} (cluster) [MeV];#eta_{s2}")(obj.cl.pt, obj.etas2)
    
    hget(name, "Rhad",      b=[(100, -0.5, 0.75)]+B,   t=";raphad"+T       )(obj.Rhad, *V)
    hget(name, "Rhad1",     b=[(100, -0.1, 0.10)]+B,   t=";raphad1"+T      )(obj.Rhad1, *V)
    
    hget(name, "reta",      b=[(60, 0.9, 1)]+B,   t=";R_{#eta}"+T          )(obj.reta, *V)
    hget(name, "rphi",      b=[(60, 0.8, 1)]+B,   t=";R_{#phi}"+T          )(obj.rphi, *V)
    
    hget(name, "Eratio",    b=[(60, 0.7, 1)]+B,   t=";E_{ratio}"+T         )(obj.Eratio, *V)
    hget(name, "DeltaE",    b=[(60, 0, 500)]+B,   t=";#DeltaE [MeV]"+T     )(obj.deltaE, *V)
    
    hget(name, "wstot",     b=[(60, 0, 5)]+B,     t=";ws_{tot}"+T   )(obj.wstot, *V)
    hget(name, "ws3",       b=[(60, 0, 1)]+B,     t=";w_{s3}"+T     )(obj.ws3, *V)
    hget(name, "fside",     b=[(80, 0, 1.25)]+B,  t=";F_{side}"+T   )(obj.fside, *V)
    
    hget(name, "Etcone20",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone20} [MeV]"+T)(obj.Etcone20, *V)
    hget(name, "Etcone30",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone30} [MeV]"+T)(obj.Etcone30, *V)
    hget(name, "Etcone40",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone40} [MeV]"+T)(obj.Etcone40, *V)
    
    hget(name, "Etcone20_pt_corrected",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone20 (corrected)} [MeV]"+T)(obj.Etcone20_pt_corrected, *V)
    hget(name, "Etcone30_pt_corrected",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone30 (corrected)} [MeV]"+T)(obj.Etcone30_pt_corrected, *V)
    hget(name, "Etcone40_pt_corrected",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone40 (corrected)} [MeV]"+T)(obj.Etcone40_pt_corrected, *V)

def plot_boson(ana, name, ph1, ph2):
    comb = ph1 + ph2
    #print comb.m
    H = ana.h.get
    if comb.m > 200000:
        # Keep all high mass events!
        ana.should_dump = True
        
    costhetastar = tanh((ph1.eta - ph2.eta) / 2)
        
    H(name, "mass",           b=[(1000, 0, 500)],     t="Boson Mass;M_{#gamma#gamma} [GeV]")(comb.m/1000)
    H(name, "mass_wide",      b=[(4000, 0, 2000)],    t="Boson Mass;M_{#gamma#gamma} [GeV]")(comb.m/1000)
    H(name, "mass_logbins",   b=[ana.mass_log_bins], t="Boson Mass;M_{#gamma#gamma} [GeV]")(comb.m/1000)
    H(name, "pt",             b=[(1000, 0, 2000)],    t="Boson p_{T};p_{T}_{#gamma#gamma} [GeV]")(comb.pt/1000)
    H(name, "eta",            b=[(100, -8, 8)],       t="Boson #eta;#eta_{#gamma#gamma}")(comb.eta)
    H(name, "phi",            b=[(100, -pi, pi)],     t="Boson #phi;#phi_{#gamma#gamma}")(comb.phi)
    H(name, "deltar",         b=[(100, 0, twopi)],    t="Boson #Delta r;#Delta r_{#gamma#gamma}")(delta_r(ph1, ph2))
    H(name, "deltaphi",       b=[(200, 0, twopi)],    t="Boson #Delta #phi;#Delta #phi_{#gamma#gamma}")(abs(ph1.phi - ph2.phi))
    H(name, "deltaeta",       b=[(100, -8, 8)],       t="Boson #Delta #eta;#Delta #eta_{#gamma#gamma}")(ph1.eta - ph2.eta)
    H(name, "costhetastar",   b=[(100, -1, 1)],       t="Boson cos(#theta^{*});cos(#theta^{*})_{#gamma#gamma}")(costhetastar)
    H(name, "boost",          b=[(100, -1, 1)],       t="Boson Boost;#beta_{Z}_{#gamma#gamma}")(tanh((ph1.eta + ph2.eta) / 2))
    
    H(name, "mass_vs_cts",   b=[ana.mass_log_bins, (50, -1, 1)], t="Boson Mass vs cos(theta*);M_{#gamma#gamma} [GeV];cos(#theta^{*})_{#gamma#gamma}")(comb.m/1000, costhetastar)
    
    H(name, "costhetastar",   b=[(100, -1, 1)],       t="Boson cos(#theta^{*});cos(#theta^{*})_{#gamma#gamma}")(tanh((ph1.eta - ph2.eta) / 2))

    if ana.mc:
        if "truth" in name or not hasattr(ph1, "truth"):
            return
        ph1t, ph2t = ph1.truth, ph2.truth
        namet = name, "truth"
        plot_boson(ana, namet, ph1t, ph2t)

def plot_boson_wconv(ana, name, ph1, ph2):
    plot_boson(ana, name, ph1, ph2)
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
            
    elif ana.project == "data11" or ana.project == "mc10":
        trigger = event.EF._2g20_loose
    
    if not trigger: return
    counts(PH_2G20L)

    if not event.is_grl: return
    counts(PH_GRL)
    
    # Requirement for other paper: and v.z < 150. 
    if not any(v.nTracks >= 3 for v in event.vertices): return
    counts(PH_VTX)
    
    return True

PHOTON_CUTFLOW = (
    "named", "total", "2g20_loose", "grl",  "vertex", "nphot", "eta", "pt", 
    "oq", "loose",   "tight",  "tightar",  "larError",  "jetcleaning")
(            PH_TOTAL, PH_2G20L,    PH_GRL, PH_VTX,   PH_N,    PH_ETA, PH_PT, 
    PH_OQ, PH_LOOSE, PH_TIGHT, PH_TIGHTAR, PH_LARERROR, PH_JETCLEANING) = range(len(PHOTON_CUTFLOW)-1)
def do_photon_cutflow(ana, event):
    counts = ana.h.get("photon_cutflow", b=[PHOTON_CUTFLOW])
    
    # Fills first four bins of `counts`
    if not pass_event(counts, ana, event):
        return
    
    good_photons = event.photons
    
    if len(good_photons) < 2: return
    counts(PH_N)
    
    # fiducal is abs(self.etas2) < 1.37 or 1.52 < abs(self.etas2) < 2.37
    good_photons = [ph for ph in good_photons if ph.pass_fiducial_eta]
    if len(good_photons) < 2: return
    counts(PH_ETA)
    
    good_photons = [ph for ph in good_photons if ph.pt_via_clE_etas2 >= 25000]
    if len(good_photons) < 2: return
    counts(PH_PT)
    
    good_photons = [ph for ph in good_photons if ph.my_oq]
    if len(good_photons) < 2: return
    counts(PH_OQ)
    
    # Plot kinematics and shower variables before loose cut, as well as after
    for ph in good_photons:
        plot_kinematics(ana, "all_phs/pre_loose", ph)
        plot_shower    (ana, "all_phs/pre_loose", ph)
        if ph.isConv:
            plot_kinematics(ana, "all_phs/pre_loose/conv", ph)
            plot_shower    (ana, "all_phs/pre_loose/conv", ph)

    good_photons = [ph for ph in good_photons if ph.loose]
    if len(good_photons) < 2: return
    counts(PH_LOOSE)
    
    for ph in good_photons:
        plot_kinematics(ana, "all_phs/post_loose", ph)
        plot_shower    (ana, "all_phs/post_loose", ph)
        if ph.isConv:
            plot_kinematics(ana, "all_phs/post_loose/conv", ph)
            plot_shower    (ana, "all_phs/post_loose/conv", ph)
    
    good_photons.sort(key=lambda o: o.pt, reverse=True)
    
    ph1, ph2 = good_photons[:2]
    
    # my_tight is robust_tight for data10, and "tight" for data11
    if ph1.my_tight and ph2.my_tight:
        counts(PH_TIGHT)
        
        # Cuts for informational purposes.
        if ph1.ambiguity_resolved and ph2.ambiguity_resolved:
            counts(PH_TIGHTAR)
            
            if not event.larError:
                counts(PH_LARERROR)
                
                if ph1.pass_jetcleaning and ph2.pass_jetcleaning:
                    counts(PH_JETCLEANING)
    
    # Loose plots
    plot_kinematics (ana, "default/ph/1", ph1)
    plot_kinematics (ana, "default/ph/2", ph2)
    plot_shower     (ana, "default/ph/1", ph1)
    plot_shower     (ana, "default/ph/2", ph2)
    plot_boson_wconv(ana, "default/ph/boson", ph1, ph2)
    
    vertex_z = event.vertices[0].z
    
    if ana.release_16:
        ph1C = ph1.v16_corrections()
        ph2C = ph2.v16_corrections()
    else:
        ph1C = ph1.v15_corrections(vertex_z)
        ph2C = ph2.v15_corrections(vertex_z)
    
    # Loose plots with corrections
    plot_kinematics (ana, "corrected/ph/1", ph1C)
    plot_kinematics (ana, "corrected/ph/2", ph2C)
    plot_boson_wconv(ana, "corrected/ph/boson", ph1C, ph2C)
    
    if ph1.my_tight and ph2.my_tight:
        plot_kinematics (ana, "corrected/ph/tight/1", ph1C)
        plot_kinematics (ana, "corrected/ph/tight/2", ph2C)
        plot_boson_wconv(ana, "corrected/ph/tight/boson", ph1C, ph2C)
        
    # Final tight plots
    for ph in good_photons:
        if ph.my_tight:
            plot_kinematics(ana, "all_phs/post_tight", ph)
            plot_shower    (ana, "all_phs/post_tight", ph)
            if ph.isConv:
                plot_kinematics(ana, "all_phs/post_tight/conv", ph)
                plot_shower    (ana, "all_phs/post_tight/conv", ph)
    
ELECTRON_CUTFLOW = (
    "named", "total",  "2g20_loose", "grl",  "vertex",  "nel", "author", "eta",  "pt", 
    "oq",  "loose",  "medium",  "blayer",  "larError",  "jetcleaning",  "tight")
(            EL_TOTAL, EL_2G20L,     EL_GRL, EL_VTX,    EL_N, EL_AUTHOR,  EL_ETA, EL_PT, 
    EL_OQ, EL_LOOSE, EL_MEDIUM, EL_BLAYER, EL_LARERROR, EL_JETCLEANING, EL_TIGHT) = range(len(ELECTRON_CUTFLOW)-1)
def do_electron_cutflow(ana, event):
    counts = ana.h.get("electron_cutflow", b=[ELECTRON_CUTFLOW])
    
    # Fills first four bins of `counts`
    if not pass_event(counts, ana, event):
        return
    
    good_electrons = event.electrons
    
    if len(good_electrons) < 2: return
    counts(EL_N)
    
    good_electrons = [el for el in good_electrons if el.author in (1, 3)]
    counts(EL_AUTHOR)
    
    # fiducal is abs(self.etas2) < 1.37 or 1.52 < abs(self.etas2) < 2.37
    good_electrons = [el for el in good_electrons if el.pass_fiducial_eta]
    if len(good_electrons) < 2: return
    counts(EL_ETA)
    
    good_electrons = [el for el in good_electrons if el.cl.pt >= 25000]
    if len(good_electrons) < 2: return
    counts(EL_PT)
    
    good_electrons = [el for el in good_electrons if el.my_oq]
    if len(good_electrons) < 2: return
    counts(EL_OQ)
    
    # Plot kinematics and shower variables before loose cut, as well as after
    for el in good_electrons:
        plot_kinematics(ana, "all_els/pre_loose", el)
        plot_shower    (ana, "all_els/pre_loose", el)

    good_electrons = [el for el in good_electrons if el.loose]
    if len(good_electrons) < 2: return
    counts(EL_LOOSE)
    
    for el in good_electrons:
        plot_kinematics(ana, "all_els/post_loose", el)
        plot_shower    (ana, "all_els/post_loose", el)
    
    good_electrons = [el for el in good_electrons if el.medium]
    if len(good_electrons) < 2: return
    counts(EL_MEDIUM)
    
    for el in good_electrons:
        plot_kinematics(ana, "all_els/post_medium", el)
        plot_shower    (ana, "all_els/post_medium", el)
    
    good_electrons = [el for el in good_electrons if el.pass_blayer_check]
    if len(good_electrons) < 2: return
    counts(EL_BLAYER)
    
    good_electrons.sort(key=lambda o: o.pt, reverse=True)
    
    el1, el2 = good_electrons[:2]
    
    if not event.larError:
        counts(EL_LARERROR)
        
        if el1.pass_jetcleaning and el2.pass_jetcleaning:
            counts(EL_JETCLEANING)
            
            if el1.tight and el2.tight:
                counts(EL_TIGHT)
    
    # Medium plots
    plot_kinematics(ana, "default/el/1", el1)
    plot_kinematics(ana, "default/el/2", el2)
    plot_shower    (ana, "default/el/1", el1)
    plot_shower    (ana, "default/el/2", el2)
    plot_boson     (ana, "default/el", el1, el2)
        
    # Final tight plots
    for el in good_electrons:
        if el.tight:
            plot_kinematics(ana, "all_els/post_tight", el)
            plot_shower    (ana, "all_els/post_tight", el)

class GravitonAnalysis(AnalysisBase):
    def __init__(self, tree, options):
    
        super(GravitonAnalysis, self).__init__(tree, options)
        
        self.ptbins = ("var", 15, 20, 25, 30, 35, 40, 50, 60, 100, 140, 180, 
                       220, 300, 380, 460, 620, 1000)
        self.ptbins = scale_bins(self.ptbins, 1000)
        
        self.ptbins_wide = "var", 15, 45, 60, 80, 120, 200, 400, 1000
        self.ptbins_wide = scale_bins(self.ptbins_wide, 1000)
        
        self.mass_log_bins = double_bins(log_binning(100, 70, 3000), 3)
        
        self.etabins_sym = "var", 0., 0.60, 1.37, 1.52, 1.81, 2.37
        self.etabins = mirror_bins(self.etabins_sym)
        self.etabins_many = double_bins(self.etabins, 3)
        
        # Tasks to run in order
        self.tasks.extend([
            do_photon_cutflow,
            do_electron_cutflow,
        ])

    def initialize_counters(self):
        self.loose_events = set()
        self.interesting_indexes = []
        
        super(GravitonAnalysis, self).initialize_counters()
        
    def flush(self):
        self.h.write_object("loose_event_indexes", self.loose_events)
        self.h.write_object("interesting", self.interesting_indexes)
        
        super(GravitonAnalysis, self).flush()

graviton_main = make_main(GravitonAnalysis)
if __name__ == "__main__":
    graviton_main()
