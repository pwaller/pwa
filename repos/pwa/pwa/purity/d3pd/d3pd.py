#! /usr/bin/env python

from minty.base import AnalysisBase
from minty.histograms import double_bins, mirror_bins, scale_bins
from minty.treedefs.egamma import Photon, Electron

from math import cosh

def pairs(inputs):
    if len(inputs) < 2:
        return
    for i, o1 in enumerate(inputs):
        for o2 in inputs[i+1:]:
            yield o1, o2
            
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
           
    pv = any(v.nTracks >= 3 for v in event.vertices)
    
    EF = event.EF
    
    ev_cuts = (event.is_grl, pv, 
       EF.g10_loose, EF.g20_loose, EF.g30_loose, EF.g40_loose, 
       EF._2g10_loose, EF._2g15_loose, EF._2g20_loose)
    
    ev_cuts_string = (
        "grl;pv;"
        # Trigger:
        "g10_loose;g20_loose;g30_loose;g40_loose;"
        "2g10_loose;2g15_loose;2g20_loose;")
    
    cut_binning = ((2, 0, 2),) * ev_cuts_string.count(";")
    fill_ev_counts = ana.h.get("event_counts", b=cut_binning, 
                            t="Event counts passing cuts;%s" % ev_cuts_string)

    fill_ev_counts(*ev_cuts)
    
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
    
    cut_binning = [(2, 0, 2)] * (len(ev_cuts) + len(each_ph_cuts))
    
    mass_binning = "var", 0, 1000, 10000, 50000, 100000, 200000
    cut_binning.append(mass_binning)
    
    all_cuts = ";".join([ev_cuts_string] + each_ph_cuts + ["first", "mass"])
    
    fill_counts = ana.h.get("diphoton_counts", b=cut_binning, 
                            t="Diphoton counts passing cuts;%s;" % all_cuts)
    
    for i, (o1, o2) in enumerate(event.diphotons):
        values = list(ev_cuts)
        for cut in diph_cuts:
            values.append(getattr(o1, cut))
            values.append(getattr(o2, cut))
            
        first = i == 0
        values.append(first)
        
        comb = o1 + o2
        values.append(comb.m)
        
        fill_counts(*values)

TITLE_SMEAR = "p_{T} smearing matrix;Truth p_{T} [MeV];Measured p_{T} [MeV]"
TITLE_SMEAR_CLUS = "p_{T} smearing matrix;Truth p_{T} [MeV];Measured (cluster) p_{T} [MeV]"

def plot_pts(ana, name, bins, obj):
    """
    Plot Pt histograms
    """
    return
    def T(what=""): return "%sp_{T};%sp_{T} [MeV];N events" % (what, what)
    
    hget = ana.h.get
    
    hget(name, "pt",    b=(bins,), t=T()          )(obj.pt)
    hget(name, "pt_cl", b=(bins,), t=T("cluster "))(obj.cl.pt)
    
    hget(name, "pt_vs_eta",    b=(bins, ana.etabins), t="cluster p_{T} vs #eta;cluster p_{T} [MeV];#eta_{S2};")(obj.cl.pt, obj.etas2)
    
    if ana.info.have_truth and obj.truth.matched:
    
        hget(name, "match_count", b=((2, 0, 2),))(obj.truth.matched)
    
        hget(name, "pt_smearmat",    b=(bins, bins), t=TITLE_SMEAR     )(obj.truth.pt, obj.pt)
        hget(name, "pt_cl_smearmat", b=(bins, bins), t=TITLE_SMEAR_CLUS)(obj.truth.pt, obj.cl.pt)
    
        hget(name, "pt_true", b=(bins,), t=T("true "))(obj.truth.pt)
        hget(name, "true_pt_vs_eta",    b=(bins, ana.etabins), t="true p_{T} vs #eta;true p_{T} [MeV];true #eta_{S2};")(obj.truth.pt, obj.truth.eta)
        
        if isinstance(obj, Photon):
            def T(what=""): return "Photon %sp_{T};%s#Deltap_{T} [MeV];N events" % (what, what)
            ptres_binning = 1000, -20000, 20000
            pt_res    = obj.truth.pt - obj.pt
            pt_cl_res = obj.truth.pt - obj.cl.pt
            
        elif isinstance(obj, Electron):
            def T(what=""): return "Electron %sp_{T};%s#Deltap_{T} [1/MeV];N events" % (what, what)
            ptres_binning = 1000, -10, 10
            name += ("reciprocal",)
            pt_res    = 1/obj.truth.pt - 1/obj.pt
            pt_cl_res = 1/obj.truth.pt - 1/obj.cl.pt
            
        else:
            raise RuntimeError("Unexpected object type")
        
        hget(name, "pt_res",    b=(ptres_binning,), t=T()         )(pt_res)
        hget(name, "pt_cl_res", b=(ptres_binning,), t=T("cluster "))(pt_cl_res)

def plot_isolation(ana, name, obj):
    hget = ana.h.get
    
    B = [ana.ptbins_wide, ana.etabins_sym]
    V = obj.cl.pt, abs(obj.etas2)
    T = ";p_{T} (cluster) [MeV];#eta_{s2}"
    
    hget(name, "et",        b=[ana.ptbins], t=";E_{T} [MeV]"          )(obj.et)
    hget(name, "pt",        b=[ana.ptbins], t=";p_{T} [MeV]"          )(obj.pt)
    hget(name, "cl_pt",     b=[ana.ptbins], t=";p_{T} (cluster) [MeV]")(obj.cl.pt)
    
    hget(name, "eta",       b=[ana.etabins], t=";#eta"                )(obj.eta)
    hget(name, "etas2",     b=[ana.etabins], t=";#eta_{s2}"           )(obj.etas2)
    
    hget(name, "et_vs_eta", b=[ana.ptbins, ana.etabins], t=";p_{T} (cluster) [MeV];#eta_{s2}")(obj.cl.pt, obj.etas2)
    
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


def plot_object(ana, name, obj):
    """
    Plot histograms for one object (electron, photon)
    """
    
    plot_isolation(ana, name, obj)

    # Make plots in bins of author
    name_auth = (name, "auth/auth_%i" % obj.author)
    plot_pts(ana, name_auth, ana.ptbins_fine, obj)
    plot_isolation(ana, name_auth, obj)
    
def plot_objects_multi_cuts(ana, name, obj):

    plot_object(ana, (name, "all"), obj)

    if obj.loose:
        plot_object(ana, (name, "loose"), obj)
    
    if obj.robust_tight:
        if obj.particle != "electron":
            assert obj.robust_nontight, "Found a tight object which isn't nontight!"
    
    if obj.particle == "photon":
        if not obj.robust_nontight: return
        plot_object(ana, (name, "nontight"), obj)
    
    if not obj.robust_tight: return
    plot_object(ana, (name, "rtight"), obj)

def fill_trigger_object_counts(ana, event):
    
    EF = event.EF
    
    triggers = [
        "g10_loose", "g20_loose", "g30_loose", "g40_loose",
        "_2g10_loose", "_2g20_loose",
    ]
    
    for trig_name in triggers:
        triggered = getattr(EF, trig_name)
        if not triggered:
            continue
        objects = getattr(EF, "%s_objects" % trig_name)
        
        ana.h.get(("photon/counts/trigphot_nocut", trig_name), b=[(15, 0, 15)])(len(objects))
        ana.h.get(("photon/counts/trigphot_tight", trig_name), b=[(15, 0, 15)])(sum(1 for o in objects if o.tight))
        
        ana.h.get(("photon/counts/allphot_nocut",  trig_name), b=[(15, 0, 15)])(len(event.photons))
        ana.h.get(("photon/counts/allphot_tight",  trig_name), b=[(15, 0, 15)])(sum(1 for o in event.photons if o.tight))
        
        for i, obj in enumerate(objects):
            if not i:
                plot_objects_multi_cuts(ana, ("photon/trigonlyfirst", trig_name), obj)
            plot_objects_multi_cuts(ana, ("photon/trig", trig_name), obj)

def plot_combined(ana, name, combined):
    hget = ana.h.get
    
    c = combined
    hget(name, "pt",  b=[ana.ptbins]           )(c.pt)
    hget(name, "eta", b=[ana.etabins_boson]          )(c.eta)
    hget(name, "eta_fine", b=[ana.etabins_boson_fine])(c.eta)
    hget(name, "phi", b=[(50, -3.141, 3.141)]  )(c.phi)
    hget(name, "m",   b=[(400, 0, 2000000)]    )(c.m)
    hget(name, "pz",  b=[(100, -1000000, 1000000)]     )(c.pz)    

def plot_phs_els_comb(ana, what, event):
    good_phs, good_els = [], []
    
    for ph in event.photons:
        if not (ph.pass_fiducial and ph.good_oq): continue
        
        good_phs.append(ph)
        
        # All photons
        plot_objects_multi_cuts(ana, (what, "photon/all"), ph)
        
        photon_type = (
            what,
            "photon",
            "sig" if ph.truth.isPhotonFromHardProc else "bkg",
            "conv" if ph.isConv else "unconv",
        )
        
        # Photons separated by sig/bkg and conversions
        plot_objects_multi_cuts(ana, photon_type, ph)
    
    for el in event.electrons:
        if not (el.pass_fiducial and el.good_oq): continue
        good_els.append(el)
        
        if el.truth.matched:
            plot_objects_multi_cuts(ana, (what, "electron/sig"), el)
        else:
            plot_objects_multi_cuts(ana, (what, "electron/bkg"), el)
    
    for comb, (ph1, ph2) in pairs_with_sum(by_pt(good_phs)):
        plot_combined(ana, (what, "boson/phs"), comb)
        
    for comb, (el1, el2) in pairs_with_sum(by_pt(good_els)):
        plot_combined(ana, (what, "boson/els"), comb)
        
    for comb, (o1, o2)   in pairs_with_sum(by_pt(good_phs + good_els)):
        plot_combined(ana, (what, "boson/both"), comb)

def plots(ana, event):
    """
    Make plots for the event
    """
    
    pv = any(v.nTracks >= 3 for v in event.vertices)
                       
    if not (pv and event.is_grl):
        # Drop these events
        return
    
    if event.EF.g10_loose:
        plot_phs_els_comb(ana, "g10_loose", event)
        
    if event.EF.g40_loose:
        plot_phs_els_comb(ana, "g40_loose", event)


class PurityAnalysis(AnalysisBase):
    def __init__(self, tree, options):
    
        super(PurityAnalysis, self).__init__(tree, options)
        
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
        
        # Tasks to run in order
        self.tasks.extend([
            counts,
            plots,
        ])
        
        if self.options.obj_selection:
            expr = "lambda o: %s" % self.options.obj_selection
            args = expr, "<options.obj_selection>", "eval"
            self.obj_selection = eval(compile(*args))
        else:
            self.obj_selection = None
        
    def finalize(self):
        super(PurityAnalysis, self).finalize()

if __name__ == "__main__":
    main(PurityAnalysis)
