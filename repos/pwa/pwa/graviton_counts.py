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
    
    if getattr(obj, "conv", None) and getattr(obj, "isConv", None) and hasattr(obj.conv, "R"):
        hget(name, "Rconv",    b=[(2000, 0, 1000)],   t="Conversion Radius;R_{conversion} [mm]")(obj.conv.R)
    
    if ana.mc:
        if "truth" in name or not hasattr(obj, "truth"): return
        objt = obj.truth
        if objt.matched:
            namet = name, "truth"
            plot_kinematics(ana, namet, objt)
            hget(namet, "mothertypes", asdict=True)(objt.mothertype)
            hget(namet, "types", asdict=True)(objt.type)
            if hasattr(objt, "deltaRRecPhoton"):
                hget(namet, "deltar", b=[(400, 0, pi)], t="Truth match #Delta r;#Delta r")(objt.deltaRRecPhoton)
            #namet = namet, str(objt.mothertype)
            #plot_kinematics(ana, namet, objt)

SIGNAL_PDGIDS = set((22, 5000039))

def plot_shower(ana, name, obj):
    hget = ana.h.get
    
    B = [ana.ptbins_wide, ana.etabins_sym]
    V = obj.cl.pt, abs(obj.etas2)
    T = ";p_{T} (cluster) [MeV];#eta_{s2}"
    
    hget(name, "et",        b=[ana.ptbins], t=";E_{T} [MeV]"          )(obj.et)
    hget(name, "cl_pt",     b=[ana.ptbins], t=";p_{T} (cluster) [MeV]")(obj.cl.pt)
    hget(name, "cl_pt_many",      b=[(500, 0, 200e3)],  t=";p_{T} (cluster) [MeV]")(obj.cl.pt)
    hget(name, "cl_pt_many_wide", b=[(2500, 0,   1e6)], t=";p_{T} (cluster) [MeV]")(obj.cl.pt)
    
    hget(name, "etas2",           b=[ana.etabins],       t=";#eta_{s2}"           )(obj.etas2)
    hget(name, "etas2_many",      b=[ana.etabins_many],  t=";#eta_{s2}"           )(obj.etas2)
    hget(name, "etas2_very_many", b=[(1000, -2.5, 2.5)], t=";#eta_{s2}"           )(obj.etas2)
    
    hget(name, "etas2_vs_phi",  b=[ana.etabins_many, PHIBINS], t=";#eta;#phi" )(obj.etas2, obj.phi)
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
    
    #hget(name, "Etcone20",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone20} [MeV]"+T)(obj.Etcone20, *V)
    #hget(name, "Etcone30",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone30} [MeV]"+T)(obj.Etcone30, *V)
    hget(name, "Etcone40",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone40} [MeV]"+T)(obj.Etcone40, *V)
    
    #hget(name, "Etcone20_pt_corrected",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone20 (corrected)} [MeV]"+T)(obj.Etcone20_pt_corrected, *V)
    #hget(name, "Etcone30_pt_corrected",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone30 (corrected)} [MeV]"+T)(obj.Etcone30_pt_corrected, *V)
    hget(name, "Etcone40_pt_corrected",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone40 (corrected)} [MeV]"+T)(obj.Etcone40_pt_corrected, *V)
   
    if hasattr(obj, "Etcone40_PtED_corrected"):
        hget(name, "Etcone40_pt_ed_corrected",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone40 (corrected)} [MeV]"+T)(obj.Etcone40_PtED_corrected(), *V)

    if ana.mc:
        if "truth" in name or not hasattr(obj, "truth"): return
        objt = obj.truth
        if objt.matched:
            namet = "fakes"
            if objt.mothertype in SIGNAL_PDGIDS:
                namet = "signal"
            elif objt.type == 22:
                namet = "nonsig_photon"
            plot_shower(ana, (name, "truth", namet), obj)
        
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

def pass_event(counts, ana, event, electron=False):
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
        EF = event.EF
        trigger = EF.e20_medium if electron else EF._2g20_loose
    
    if not trigger: return
    counts(PH_2G20L)
    
    # In good run list
    if not event.is_grl: return
    counts(PH_GRL)
    
    # Requirement for other paper: and v.z < 150. 
    if not any(v.nTracks >= 3 for v in event.vertices): return
    counts(PH_VTX)
    
    return True

def plot_all(ana, name, ph1, ph2):
    plot_kinematics (ana, ("default/ph", name, "1"), ph1)
    plot_kinematics (ana, ("default/ph", name, "2"), ph2)
    plot_shower     (ana, ("default/ph", name, "1"), ph1)
    plot_shower     (ana, ("default/ph", name, "2"), ph2)
    plot_boson_wconv(ana, ("default/ph", name, "boson"), ph1, ph2)
    
def plot_all_el(ana, name, ph1, ph2):
    plot_kinematics(ana, ("default/el", name, "1"), ph1)
    plot_kinematics(ana, ("default/el", name, "2"), ph2)
    plot_shower    (ana, ("default/el", name, "1"), ph1)
    plot_shower    (ana, ("default/el", name, "2"), ph2)
    plot_boson     (ana, ("default/el", name, "boson"), ph1, ph2)

def plot_kinematics_shower(ana, name, obj, conv=False):
    plot_kinematics(ana, name, obj)
    plot_shower    (ana, name, obj)
    if conv:
        conv = "conv" if obj.isConv else "unconv"
        plot_kinematics(ana, (name, conv), obj)
        plot_shower    (ana, (name, conv), obj)    

PHOTON_CUTFLOW = (
    "named", "total", "2g20_loose", "grl",  "vertex", "nphot", "eta", "pt", 
    "oq", "phcleaning",       "loose",   "tight",  "iso < 5 GeV", "Remove ee", "mass > 120 GeV", "larError", "tightar")
(            PH_TOTAL, PH_2G20L,    PH_GRL, PH_VTX,   PH_N,    PH_ETA, PH_PT, 
    PH_OQ, PH_PHOTONCLEANING, PH_LOOSE, PH_TIGHT,  PH_ISOLATION,  PH_NOT_EE,   PH_MASS,          PH_LARERROR, PH_TIGHTAR) = range(len(PHOTON_CUTFLOW)-1)
def do_photon_cutflow(ana, event, is_ee_candidate):
    counts = ana.h.get("photon_cutflow", b=[PHOTON_CUTFLOW])
    
    good_photons = event.photons
    
    for ph in good_photons:
        plot_kinematics_shower(ana, "all_phs/0_pre_everything", ph, True)
    
    # Event cuts
    # Fills first four bins of `counts`
    if not pass_event(counts, ana, event):
        return
        
    for ph in good_photons:
        plot_kinematics_shower(ana, "all_phs/1_pre_fiducial", ph, True)
    
    if len(good_photons) < 2: return
    counts(PH_N)
    
    # fiducal is abs(self.etas2) < 1.37 or 1.52 < abs(self.etas2) < 2.37
    good_photons = [ph for ph in good_photons if ph.pass_fiducial_eta]
    if len(good_photons) < 2: return
    counts(PH_ETA)
    
    # Compute the corrections
    vertex_z = event.vertices[0].z
    for ph in good_photons:
        ph.compute_corrected(vertex_z)
    
    # 25 GeV pt cut
    good_photons = [ph for ph in good_photons if ph.corrected.pt >= 25000]
    if len(good_photons) < 2: return
    counts(PH_PT)
    
    # OTX check
    good_photons = [ph for ph in good_photons if ph.my_oq]
    if len(good_photons) < 2: return
    counts(PH_OQ)
    
    # Check photon cleaning
    good_photons = [ph for ph in good_photons if ph.pass_photoncleaning]
    if len(good_photons) < 2: return
    counts(PH_PHOTONCLEANING)    
    
    # Plot kinematics and shower variables before loose cut, as well as after
    for ph in good_photons:
        plot_kinematics_shower(ana, "all_phs/2_pre_loose", ph, True)

    # Remove non-loose candidates
    good_photons = [ph for ph in good_photons if ph.loose]
    if len(good_photons) < 2: return
    counts(PH_LOOSE)
    
    for ph in good_photons:
        plot_kinematics_shower(ana, "all_phs/3_post_loose", ph, True)
    
    good_photons.sort(key=lambda o: o.pt, reverse=True)
    
    ## Diphoton plots
    ph1, ph2 = good_photons[:2]
    
    # Loose plots
    plot_all(ana, "loose", ph1, ph2)
    
    nontight = [ph for ph in good_photons if ph.nontight and not ph.my_tight]
    
    if len(nontight) >= 2:
        ph1, ph2 = nontight[:2]
        # Plot nontight-nontight
        plot_all(ana, "nontight_nontight", ph1, ph2)
        
    ## More cuts
    
    # my_tight is robust_tight for data10, and "tight" for data11
    good_photons = [ph for ph in good_photons if ph.my_tight]
    
    for ph in good_photons:
        plot_kinematics_shower(ana, "all_phs/4_post_tight", ph, True)
    
    if nontight and good_photons:
        # Plot tight-antitight
        ph1, ph2 = good_photons[0], nontight[0]
        plot_all(ana, "tight_nontight", ph1, ph2)
    
    if len(good_photons) < 2: return
    counts(PH_TIGHT)
    
    # Isolation cut
    good_photons = [ph for ph in good_photons if ph.Etcone40_PtED_corrected() < 5000]
    if len(good_photons) < 2: return
    counts(PH_ISOLATION)
    
    for ph in good_photons:
        plot_kinematics_shower(ana, "all_phs/5_post_iso", ph, True)
        
    # Remove ee candidates, record run/event
    if is_ee_candidate:
        ana.gg_cand_has_ee.append((event.RunNumber, event.EventNumber))
        return
    counts(PH_NOT_EE)
    
    ## Select best diphoton pair again (leading an subleading due to sort earlier)
    ph1, ph2 = good_photons[:2]
    
    plot_all(ana, "tight", ph1, ph2)
    
    # Vertex and enery correction
    ph1C, ph2C = ph1.corrected, ph2.corrected
    
    if ph1.my_tight and ph2.my_tight:
        plot_kinematics (ana, "corrected/ph/tight/1", ph1C)
        plot_kinematics (ana, "corrected/ph/tight/2", ph2C)
        plot_boson_wconv(ana, "corrected/ph/tight/boson", ph1C, ph2C)
        
        mass = (ph1C + ph2C).m
        
        if mass >= 120000:
            counts(PH_MASS)
            ana.good_events.append((event.RunNumber, event.EventNumber))
            ana.mass_values.append(mass)
            
            plot_all(ana, "mass_cut", ph1, ph2)
            plot_kinematics (ana, "corrected/ph/mass_cut/1", ph1C)
            plot_kinematics (ana, "corrected/ph/mass_cut/2", ph2C)
            plot_boson_wconv(ana, "corrected/ph/mass_cut/boson", ph1C, ph2C)
            
            if not event.larError:
                counts(PH_LARERROR)
                
                # Cuts for informational purposes.
                if ph1.ambiguity_resolved and ph2.ambiguity_resolved:
                    counts(PH_TIGHTAR)
    
    return True
    
ELECTRON_CUTFLOW = (
    "named", "total",  "e20_medium", "grl",  "vertex",  "nel", "author", "eta",  "pt", 
    "oq",  "loose",  "medium",  "blayer",  "iso < 7 GeV", "mass > 120 GeV",  "larError",  "tight")
(            EL_TOTAL, EL_2G20L,     EL_GRL, EL_VTX,    EL_N, EL_AUTHOR,  EL_ETA, EL_PT, 
    EL_OQ, EL_LOOSE, EL_MEDIUM, EL_BLAYER, EL_ISOLATION,  EL_MASS,           EL_LARERROR, EL_TIGHT) = range(len(ELECTRON_CUTFLOW)-1)
def do_electron_cutflow(ana, event):
    counts = ana.h.get("electron_cutflow", b=[ELECTRON_CUTFLOW])
    
    good_electrons = event.electrons
    
    for el in good_electrons:
        plot_kinematics_shower(ana, "all_els/0_pre_everything", el)
        
    # Fills first four bins of `counts`
    if not pass_event(counts, ana, event, electron=True):
        return
    
    if len(good_electrons) < 2: return
    counts(EL_N)
    
    good_electrons = [el for el in good_electrons if el.author in (1, 3)]
    if len(good_electrons) < 2: return
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
        plot_kinematics_shower(ana, "all_els/1_pre_loose", el)

    good_electrons = [el for el in good_electrons if el.loose]
    if len(good_electrons) < 2: return
    counts(EL_LOOSE)
    
    for el in good_electrons:
        plot_kinematics_shower(ana, "all_els/2_post_loose", el)
    
    good_electrons.sort(key=lambda o: o.pt, reverse=True)
    el1, el2 = good_electrons[:2]
    plot_all_el(ana, "loose", el1, el2)
    
    good_electrons = [el for el in good_electrons if el.medium]
    if len(good_electrons) < 2: return
    counts(EL_MEDIUM)
    
    for el in good_electrons:
        plot_kinematics_shower(ana, "all_els/3_post_medium", el)
    
    good_electrons = [el for el in good_electrons if el.pass_blayer_check]
    if len(good_electrons) < 2: return
    counts(EL_BLAYER)
    
    nvx_with_tracks = sum(1 for v in event.vertices if v.nTracks >= 2)
    
    good_electrons = [el for el in good_electrons 
                      if el.EtCone20_ptNPV_corrected(nvx_with_tracks) < 7000]
    if len(good_electrons) < 2: return
    counts(EL_ISOLATION)
    
    el1, el2 = good_electrons[:2]
    
    if (el1 + el2).m < 120000: return
    counts(EL_MASS)
    
    if not event.larError:
        counts(EL_LARERROR)
            
        if el1.tight and el2.tight:
            counts(EL_TIGHT)
    
    plot_all_el(ana, "medium", el1, el2)
    
    # Final tight plots
    for el in good_electrons:
        if el.tight:
            plot_kinematics_shower(ana, "all_els/4_post_tight", el)
            
    return True

def do_cutflows(ana, event):
    is_ee_candidate = do_electron_cutflow(ana, event)
    do_photon_cutflow(ana, event, is_ee_candidate)
    

class GravitonAnalysis(AnalysisBase):
    def __init__(self, tree, options):
    
        super(GravitonAnalysis, self).__init__(tree, options)
        
        self.ptbins = ("var", 15, 20, 25, 30, 35, 40, 50, 60, 100, 140, 180, 
                       220, 300, 380, 460, 620, 1000)
        self.ptbins = scale_bins(self.ptbins, 1000)
        
        self.ptbins_wide = "var", 15, 45, 60, 80, 120, 200, 400, 1000
        self.ptbins_wide = scale_bins(self.ptbins_wide, 1000)
        
        self.mass_log_bins_smaller = log_binning(10, 70, 3000)
        self.mass_log_bins_small = log_binning(100, 70, 3000)
        self.mass_log_bins = double_bins(self.mass_log_bins_small, 3)
        
        self.etabins_sym = "var", 0., 0.60, 1.37, 1.52, 1.81, 2.37
        self.etabins = mirror_bins(self.etabins_sym)
        self.etabins_many = double_bins(self.etabins, 3)
        
        # Tasks to run in order
        self.tasks.extend([
            do_cutflows,
        ])

    def initialize_counters(self):
        self.loose_events = set()
        self.interesting_indexes = []
        self.gg_cand_has_ee = []
        self.good_events = []
        self.mass_values = []
        
        super(GravitonAnalysis, self).initialize_counters()
        
    def flush(self):
        self.h.write_object("loose_event_indexes", self.loose_events)
        self.h.write_object("interesting", self.interesting_indexes)
        self.h.write_object("gg_cand_has_ee", self.gg_cand_has_ee)
        self.h.write_object("good_events", self.good_events)
        self.h.write_object("mass_values", self.mass_values)
        
        super(GravitonAnalysis, self).flush()

graviton_main = make_main(GravitonAnalysis)
if __name__ == "__main__":
    graviton_main()
