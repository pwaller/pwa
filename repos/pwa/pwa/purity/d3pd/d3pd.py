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
        "2g10_loose;2g15_loose;2g20_loose")
    
    cut_binning = ((2, 0, 2),) * len(ev_cuts_string.split(";"))
    fill_ev_counts = ana.h.get("event_counts", b=cut_binning, 
                            t="Event counts passing cuts;%s;" % ev_cuts_string)

    fill_ev_counts(*ev_cuts)
          
    cuts = ("loose;nontight;tight;robust_nontight;robust_tight;"
        "pt_gt40;pt_gt100;pt_gt200;pt_gt500;isolated;nonisolated;"
        "fiducial;oq;isConv;"
        ) + ev_cuts_string
    cut_binning = ((2, 0, 2),) * len(cuts.split(";"))
    fill_counts = ana.h.get("photon_counts", b=cut_binning, 
                            t="Photon counts passing cuts;%s;" % cuts)
    
    for o in event.photons:
        fill_counts(o.loose, o.nontight, o.tight, o.robust_nontight, o.robust_tight, 
                    o.cl.pt > 40000, o.cl.pt > 100000, o.cl.pt > 200000, o.cl.pt > 500000, 
                    o.isolated, o.nonisolated,
                    o.pass_fiducial, o.good_oq, o.isConv,
                    *ev_cuts)
    
    diph_cuts = "good_oq;pass_fiducial;loose;robust_nontight;robust_tight;nonisolated;isolated;isConv".split(";")
    
    cuts = []
    for c in diph_cuts:
        cuts.append(c + "_1")
        cuts.append(c + "_2")
    
    all_cuts = ";".join([ev_cuts_string] + cuts)
    cut_binning = ((2, 0, 2),) * (len(ev_cuts) + len(cuts))
    fill_counts = ana.h.get("diphoton_counts", b=cut_binning, 
                            t="Diphoton counts passing cuts;%s;" % all_cuts)
        
    ph_by_pt = sorted(event.photons, key=lambda p: p.pt)
    for o1, o2 in pairs(ph_by_pt):
        values = list(ev_cuts)
        for cut in diph_cuts:
            values.append(getattr(o1, cut))
            values.append(getattr(o2, cut))
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
    
    hget(name, "et",        b=[ana.ptbins],     t=";E_{T} [MeV]"        )(obj.et)
    hget(name, "etas2",     b=[ana.etabins],    t=";#eta_{s2}"          )(obj.etas2)
    hget(name, "Rhad",      b=[(100, -0.5, 0.75)],   t=";raphad"        )(obj.Rhad)
    hget(name, "Rhad1",     b=[(100, -0.1, 0.10)],   t=";raphad1"       )(obj.Rhad1)
    
    hget(name, "reta",      b=[(20, 0.9, 1)] ,  t=";R_{#eta}"           )(obj.reta)
    hget(name, "rphi",      b=[(15, 0.8, 1)],   t=";R_{#phi}"           )(obj.rphi)
    
    hget(name, "Eratio",    b=[(15, 0.7, 1)],   t=";E_{ratio}"          )(obj.Eratio)
    hget(name, "DeltaE",    b=[(15, 0, 500)],   t=";#DeltaE [MeV]"      )(obj.deltaE)
    
    hget(name, "wstot",     b=[(15, 0, 5)],     t=";ws_{tot}"    )(obj.wstot)
    hget(name, "ws3",       b=[(15, 0, 1)],     t=";w_{s3}"      )(obj.ws3)
    hget(name, "fside",     b=[(20, 0, 1.25)],  t=";F_{side}"    )(obj.fside)
    
    hget(name, "EtCone20",  b=[(100, -5000, 50000)], t=";E_{T}^{cone20} [MeV]")(obj.EtCone20)
    hget(name, "EtCone30",  b=[(100, -5000, 50000)], t=";E_{T}^{cone30} [MeV]")(obj.EtCone30)
    hget(name, "EtCone40",  b=[(100, -5000, 50000)], t=";E_{T}^{cone40} [MeV]")(obj.EtCone40)
    
    hget(name, "EtCone20_corrected",  b=[(100, -5000, 50000)], t=";E_{T}^{cone20 (corrected)} [MeV]")(obj.EtCone20_corrected)
    hget(name, "EtCone30_corrected",  b=[(100, -5000, 50000)], t=";E_{T}^{cone30 (corrected)} [MeV]")(obj.EtCone30_corrected)
    hget(name, "EtCone40_corrected",  b=[(100, -5000, 50000)], t=";E_{T}^{cone40 (corrected)} [MeV]")(obj.EtCone40_corrected)


def plot_object(ana, name, obj):
    """
    Plot histograms for one object (electron, photon)
    """
    
    #plot_pts(ana, (name, "eta_all"), ana.ptbins,      obj)
    #plot_pts(ana, (name, "fine"),    ana.ptbins_fine, obj)
    
    plot_isolation(ana, name, obj)
    
    # Make pt plots in bins of eta
    for i, (elow, ehi) in enumerate(zip(ana.etabins_sym[1:], ana.etabins_sym[2:])):
        if not elow <= obj.etas2 < ehi:
            continue
        name_eta = (name, "eta_%i" % i)
        plot_pts(ana, name_eta, ana.ptbins, obj)
        plot_isolation(ana, name_eta, obj)

    # Make plots in bins of author
    name_auth = (name, "auth_%i" % obj.author)
    plot_pts(ana, name_auth, ana.ptbins_fine, obj)
    plot_isolation(ana, name_auth, obj)
    
def plot_objects_multi_cuts(ana, name, obj):

    plot_object(ana, (name, "loose"), obj)
    if obj.robust_tight:
        assert obj.robust_nontight, "Found a tight object which isn't nontight!"
        
    if not obj.robust_nontight: return
    plot_object(ana, (name, "nontight"), obj)
    
    if not obj.robust_tight: return
    plot_object(ana, (name, "rtight"), obj)

def plot_objects_multi_pt(ana, name, obj):
    plot_objects_multi_cuts(ana, (name, "ptcl_all"), obj)
    
    if obj.cl.pt > 100000:
        plot_objects_multi_cuts(ana, (name, "ptcl_gt100"), obj)
    elif obj.cl.pt > 40000:
        plot_objects_multi_cuts(ana, (name, "ptcl_gt40"), obj)
    else:
        plot_objects_multi_cuts(ana, (name, "ptcl_lte40"), obj)

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
        
        ana.h.get(("photon_count_trigphot_nocut", trig_name), b=[(15, 0, 15)])(len(objects))
        ana.h.get(("photon_count_trigphot_tight", trig_name), b=[(15, 0, 15)])(sum(1 for o in objects if o.tight))
        
        ana.h.get(("photon_count_allphot_nocut",  trig_name), b=[(15, 0, 15)])(len(event.photons))
        ana.h.get(("photon_count_allphot_tight",  trig_name), b=[(15, 0, 15)])(sum(1 for o in event.photons if o.tight))
        
        for i, obj in enumerate(objects):
            if not i:
                plot_objects_multi_pt(ana, ("photontrigonlyfirst", trig_name), obj)
            plot_objects_multi_pt(ana, ("photontrig", trig_name), obj)

def plots(ana, event):
    """
    Make plots for the event
    """
    # Could do a loop over [("electron", ph.electrons), ("photon", ph.photons)]
    # but left it expanded as two loops just to get an idea what it looks like
    
    pv = any(v.nTracks >= 3 for v in event.vertices)
    
    any_trigger = any((event.EF.g10_loose, event.EF.g20_loose, 
                       event.EF.g30_loose, event.EF.g40_loose))
                       
    if not all((pv, event.is_grl, any_trigger)): return
    
    fill_trigger_object_counts(ana, event)
    
    for ph in event.photons:
        if not (ph.pass_fiducial and ph.loose and ph.good_oq): continue
        if ana.obj_selection and not ana.obj_selection(ph):
            continue
        
        plot_objects_multi_pt(ana, "photon", ph)
        
        if ph.isConv:
            plot_objects_multi_pt(ana, "convphoton", ph)
        else:
            plot_objects_multi_pt(ana, "unconvphoton", ph)
            

class PurityAnalysis(AnalysisBase):
    def __init__(self, tree, options):
    
        super(PurityAnalysis, self).__init__(tree, options)
        
        self.ptbins = ("var", 15, 20, 25, 30, 35, 40, 50, 60, 100, 140, 180, 
                       220, 300, 380, 460, 620, 1000)
        self.ptbins = scale_bins(self.ptbins, 1000)
        self.etabins_sym = "var", 0., 0.60, 1.37, 1.52, 1.81, 2.37
        self.etabins = mirror_bins(self.etabins_sym)
        
        self.ptbins_fine  = double_bins(self.ptbins,  4)
        self.etabins_fine = double_bins(self.etabins, 4)
        
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