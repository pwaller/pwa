#! /usr/bin/env python

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
            
def by_pt(objects):
    return sorted(objects, key=lambda o: o.pt)

def counts(ana, event):
    """
    Fill a sparse histogram for counting cuts (allows one
    """
           
    # There exists a vertex with at least 3 tracks and Pz < 150mm
    pv = any(v.nTracks >= 3 and v.z < 150. for v in event.vertices)
    good_phs = [ph for ph in event.photons if ph.graviton2011_fiducial]
    
    
    
    EF = event.EF
    
    ev_cuts = (event.is_grl, pv, len(good_phs) >= 2,
       EF.g10_loose, EF.g20_loose, EF.g30_loose, EF.g40_loose, 
       EF._2g10_loose, EF._2g15_loose, EF._2g20_loose)
    
    ev_cuts_string = (
        "grl;pv;have_good_diph;"
        # Trigger:
        "g10_loose;g20_loose;g30_loose;g40_loose;"
        "2g10_loose;2g15_loose;2g20_loose;")
    
    cut_binning = ((2, 0, 2),) * ev_cuts_string.count(";")
    fill_ev_counts = ana.h.get("event_counts", b=cut_binning, 
                            t="Event counts passing cuts;%s" % ev_cuts_string)

    fill_ev_counts(*ev_cuts)
    
    return
    
    cuts = ("loose;nontight;tight;robust_nontight;robust_tight;"
        "pt_gt40;pt_gt100;pt_gt200;pt_gt500;isolated;nonisolated;"
        "fiducial;oq;isConv;isPhotonFromHardProc;"
        ) + ev_cuts_string
    cut_binning = ((2, 0, 2),) * cuts.count(";")
    fill_counts = ana.h.get("photon_counts", b=cut_binning, 
                            t="Photon counts passing cuts;%s" % cuts)
    
    for o in event.photons:
        fill_counts(o.loose, o.nontight, o.tight, o.robust_nontight, o.robust_tight, 
                    o.cl.pt > 40000, o.cl.pt > 100000, o.cl.pt > 200000, o.cl.pt > 500000, 
                    o.isolated, o.nonisolated,
                    o.pass_fiducial, o.good_oq, o.isConv, o.truth.isPhotonFromHardProc,
                    *ev_cuts)
    
    cuts = ("loose;nontight;tight;robust_nontight;robust_tight;"
        "pt_gt40;pt_gt100;pt_gt200;pt_gt500;isolated;nonisolated;"
        "fiducial;oq;isConv;matchMC;"
        ) + ev_cuts_string
    cut_binning = ((2, 0, 2),) * cuts.count(";")
    el_fill_counts = ana.h.get("electron_counts", b=cut_binning, 
                               t="Electron counts passing cuts;%s" % cuts)
                               
    for o in event.electrons:
        el_fill_counts(o.loose, 0, o.tight, 0, o.robust_tight, 
            o.cl.pt > 40000, o.cl.pt > 100000, o.cl.pt > 200000, o.cl.pt > 500000, 
            o.isolated, o.nonisolated,
            o.pass_fiducial, o.good_oq, 0, o.truth.matched,
            *ev_cuts)
    
    diph_cuts = "good_oq;pass_fiducial;loose;robust_nontight;robust_tight;nonisolated;isolated;isConv".split(";")
    
    each_ph_cuts = []
    for c in diph_cuts:
        each_ph_cuts.append(c + "_1")
        each_ph_cuts.append(c + "_2")
    
    cut_binning = [(2, 0, 2)] * (len(ev_cuts) + len(each_ph_cuts) + 1)
            
    fill_counts = ana.h.get("diphoton_counts", b=cut_binning, 
                            t="Diphoton counts passing cuts;%s;" % all_cuts)
    
    for i, (o1, o2) in enumerate(event.diphotons):
        values = list(ev_cuts)
        for cut in diph_cuts:
            values.append(getattr(o1, cut))
            values.append(getattr(o2, cut))
        
        fill_counts(*values)

def plot_combined(ana, name, combined):
    hget = ana.h.get
    
    c = combined
    hget(name, "pt",  b=[ana.ptbins]           )(c.pt)
    hget(name, "eta", b=[ana.etabins_boson]          )(c.eta)
    hget(name, "eta_fine", b=[ana.etabins_boson_fine])(c.eta)
    hget(name, "phi", b=[(50, -3.141, 3.141)]  )(c.phi)
    hget(name, "m",   b=[(800, 0, 2000000)], t=";M_{#gamma#gamma} [MeV]")(c.m)
    hget(name, "pz",  b=[(100, -1000000, 1000000)]     )(c.pz)

S_leading, S_leading_er = 0.1, 0.2
C_leading, C_leading_er_B, C_leading_er_EC = 0.007, 1, 4

def apply_correction(ph):
 
    energy = ph.E
    sqrt_energy = sqrt(energy)
 
    C_leading_er = C_leading_er_B if ph.in_barrel else C_leading_er_EC

    sigma0 = sqrt( 
        +pow(S_leading * (1 + S_leading_er)  * sqrt_energy, 2)
        +pow(C_leading * (1 + C_leading_er) *       energy, 2)
        -pow(S_leading * sqrt_energy, 2)
        -pow(C_leading *      energy, 2))

    DeltaE0 = gRandom.Gaus(0, sigma0)
    
    ph.E += DeltaE0
    return sigma0, DeltaE0

def combine(ph1, ph2):
    return ph1 + ph2

def plot_phs_els_comb(ana, event):

    if not event.is_grl or not any(v.nTracks >= 3 and v.z < 150. for v in event.vertices):
        return

    good_phs = by_pt(ph for ph in event.photons if ph.graviton2011_fiducial)
                
    if len(good_phs) < 2: return
    
    hm = ana.h.get
    
    ph1, ph2 = good_phs[:2]
    
    pos = ph1.region_character + ph2.region_character
    comb = combine(ph1, ph2)

    plot_combined(ana, "boson/phs/all", comb)
    plot_combined(ana, "boson/phs/%s" % pos, comb)

    m1b, m2b, comb_pre = ph1.m, ph2.m, comb.m

    s1, c1 = apply_correction(ph1.cl)
    s2, c2 = apply_correction(ph2.cl)
    
    comb = combine(ph1, ph2)
    m1d, m2d, comb_delta = m1b - ph1.m, m2b - ph2.m, comb_pre - comb.m
    
    hm("s1", t="S1;S1", b=[(101, -600000, 600000)])(s1)
    hm("c1", t="C1;C1", b=[(101, -150000, 150000)])(c1)
    hm("s2", t="S2;S2", b=[(101, -600000, 600000)])(s2)
    hm("c2", t="C2;C2", b=[(101, -150000, 150000)])(c2)
    #hm.get("m1d", "Mass Delta;M_{#gamma#gamma} (corr) - M_{#gamma#gamma}", b=[(101, -600000, 600000)])
    hm("mdelta", "Mass Delta;M_{#gamma#gamma} (corr) - M_{#gamma#gamma}", b=[(101, -300000, 300000)])
    
    ana.tup.Fill(s1, c1, m1d, s2, c2, m2d, comb_delta)
    #raise RuntimeError("s1 %.2e, c1 %.2e, m1d %.2e, s2 %.2e, s2c %.2e, m2d %.2e = " % (s1, c1, m1d, c2, s2, m2d))
    
    plot_combined(ana, "boson/phs_corr/all", comb)
    plot_combined(ana, "boson/phs_corr/%s" % pos, comb)


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
        self.etabins_boson = mirror_bins(self.etabins_sym + (3., 3.6, 4.2, 5.))
        
        self.ptbins_fine  = double_bins(self.ptbins,  4)
        self.etabins_fine = double_bins(self.etabins, 4)
        self.etabins_boson_fine = double_bins(self.etabins_boson, 4)

        self.tup = TNtuple("smearvars", "smearing variables", "s1:c1:m1d:s2:c2:m2d:mdelta")

        # Tasks to run in order
        self.tasks.extend([
            counts,
            plot_phs_els_comb,
        ])

    def finalize(self):
        self.h.file.cd()
        self.tup.Write()
        super(GravitonAnalysis, self).finalize()

graviton_main = make_main(GravitonAnalysis)    
if __name__ == "__main__":
    graviton_main()
