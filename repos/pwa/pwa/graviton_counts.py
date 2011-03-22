#! /usr/bin/env python

from logging import getLogger; log = getLogger("pwa.graviton_counts")

from math import cosh, sqrt

from ROOT import gRandom, TNtuple

from minty.base import AnalysisBase
from minty.histograms import double_bins, mirror_bins, scale_bins
from minty.main import make_main
from minty.treedefs.egamma import Photon, Electron

def pairs_with_sum(inputs):
    if len(inputs) < 2:
        return
    for i, o1 in enumerate(inputs):
        for o2 in inputs[i+1:]:
            yield o1+o2, (o1, o2)

def plot_kinematics(ana, name, obj):
    hget = ana.h.get

    hget(name, "E",         b=[ana.ptbins],    t=";E [MeV]"       )(obj.E)
    
    hget(name, "pt",         b=[ana.ptbins],    t=";p_{T} [MeV]"       )(obj.pt)
    hget(name, "pt_many",    b=[(500, 0, 200e3)], t=";p_{T} [MeV]"       )(obj.pt)
    
    hget(name, "eta",        b=[ana.etabins], t=";#eta"                )(obj.eta)
    hget(name, "eta_many",   b=[ana.etabins_many], t=";#eta"           )(obj.eta)
    
    hget(name, "phi",        b=[(100, -3.1415, 3.1415)], t=";#phi"     )(obj.phi)

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
    
    hget(name, "EtCone20",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone20} [MeV]"+T)(obj.EtCone20, *V)
    hget(name, "EtCone30",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone30} [MeV]"+T)(obj.EtCone30, *V)
    hget(name, "EtCone40",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone40} [MeV]"+T)(obj.EtCone40, *V)
    
    hget(name, "EtCone20_corrected",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone20 (corrected)} [MeV]"+T)(obj.EtCone20_corrected, *V)
    hget(name, "EtCone30_corrected",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone30 (corrected)} [MeV]"+T)(obj.EtCone30_corrected, *V)
    hget(name, "EtCone40_corrected",  b=[(100, -5000, 50000)]+B, t=";E_{T}^{cone40 (corrected)} [MeV]"+T)(obj.EtCone40_corrected, *V)

def plot_boson(ana, name, ph1, ph2):
    comb = ph1 + ph2
    #print comb.m
    H = ana.h.get
    H(name, "boson/mass", b=[(1000, 0, 500)], t=";M_{#gamma#gamma} [GeV]")(comb.m/1000)
    H(name, "boson/eta",  b=[(100, -8, 8)])(comb.eta)
    H(name, "boson/phi",  b=[(100, -3.1415, 3.1415)])(comb.phi)

def plot_boson_wconv(ana, name, ph1, ph2):
    plot_boson(ana, name, ph1, ph2)
    if ph1.isConv or ph2.isConv:
        plot_boson(ana, (name, "conveither"), ph1, ph2)
    if ph1.isConv and ph2.isConv:
        plot_boson(ana, (name, "convboth"), ph1, ph2)

CUTFLOW = ("named", "total", "trigger", "grl", "vertex", "nphot", "eta", "pt", 
           "oq", "jetclean", "loose", "tight")
def do_cutflow(ana, event):
    counts = ana.h.get("cutflow", b=[CUTFLOW])
    
    # Total
    counts(0)
    
    # Pass GRL
    if not event.is_grl: return
    counts(1)
    
    # Pass vertex
    # Requirement for other paper: and v.zvertex < 150. 
    if not any(v.nTracks >= 3 for v in event.vertices):
        return
    counts(2)
    
    # Pass Trigger
    if event.RunNumber < 160889:
        # The above cut (event.RunNumber < 160889) also catches MC.
        trigger = any(ph.L1_e >= 14000 for ph in event.photons)
        #event.L1.EM14
    else:
        trigger = event.EF._2g15_loose or event.EF.e20_loose
    
    if not trigger: return
    counts(3)
    
    good_photons = event.photons
    
    # Pass nphot
    if len(good_photons) < 2: return
    counts(4)
    
    good_photons = [ph for ph in good_photons if ph.pass_fiducial_eta]
    if len(good_photons) < 2: return
    counts(5)
    
    good_photons = [ph for ph in good_photons if ph.pass_fiducial_pt]
    if len(good_photons) < 2: return
    counts(6)
    
    # Pass object quality
    good_photons = [ph for ph in good_photons if ph.good_oq]
    
    if len(good_photons) < 2: return
    counts(7)
    
    # Pass jet cleaning
    good_photons = [ph for ph in good_photons if ph.good_jet_quality]
    if len(good_photons) < 2: return
    counts(8)

    for ph in good_photons:
        plot_kinematics(ana, "good_phs", ph)
        plot_shower(ana, "good_phs", ph)

    # Pass looseness
    good_photons = [ph for ph in good_photons if ph.loose]
    if len(good_photons) < 2: return
    counts(9)
    
    ana.loose_events.add((event.RunNumber, event.LumiBlock, event.EventNumber))
    
    # Pass tightness
    if sum(1 for ph in good_photons if ph.robust_tight) >= 2:
        counts(10)
    
    ph1, ph2 = good_photons[:2]
    
    plot_kinematics(ana, "default/ph1", ph1)
    plot_kinematics(ana, "default/ph2", ph2)
    plot_boson_wconv(ana, "default", ph1, ph2)
    plot_shower(ana, "default/ph1", ph1)
    plot_shower(ana, "default/ph2", ph2)
    
    vertex_z = event.vertices[0].zvertex
    
    if ana.release_16:
        ph1C = ph1.v16_corrections()
        ph2C = ph2.v16_corrections()
    else:
        ph1C = ph1.v15_corrections(vertex_z)
        ph2C = ph2.v15_corrections(vertex_z)
    
    plot_kinematics(ana, "corrected/ph1", ph1C)
    plot_kinematics(ana, "corrected/ph2", ph2C)
    plot_boson_wconv(ana, "corrected", ph1C, ph2C)
    
class GravitonAnalysis(AnalysisBase):
    def __init__(self, tree, options):
    
        super(GravitonAnalysis, self).__init__(tree, options)
        
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
            do_cutflow,
        ])

    def initialize_counters(self):
        self.loose_events = set()
        self.interesting_indexes = []
        
        super(GravitonAnalysis, self).initialize_counters()
        
    def flush(self):
        self.h.write_object("loose_event_indexes", self.loose_events)
        self.h.write_object("interesting", self.interesting_indexes)
        
        super(GravitonAnalysis, self).flush()


    def finalize(self):
    
        super(GravitonAnalysis, self).finalize()

graviton_main = make_main(GravitonAnalysis)    
if __name__ == "__main__":
    graviton_main()
