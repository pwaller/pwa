#! /usr/bin/env python

from os import makedirs
from os.path import exists, isdir, join as pjoin

import ROOT as R
from minty.histograms import fixup_hist_units

# Safety
R.TH3.Project3D._creates = True

input_2011 = "../results/51/all.root"

def additional_processing(hname, hists):
    with_log = False
    if "mass" in hname:
        hists = [h.Rebin(10) for h in hists]
        with_log = True
        
    elif "cone" in hname:
        with_log = True
        
    elif ("pt" in hname or hname in ["E", "et"]) and (not "_vs" in hname and not "cone" in hname):
        if not hists[0].GetXaxis().IsVariableBinSize():
            hists = [h.Rebin(5) for h in hists]
            if "wide" in hname:
                hists = [h.Rebin(2) for h in hists]
        with_log = True

    elif "had" in hname:
        for h in hists:
            h.GetXaxis().SetRangeUser(-0.2, 0.2)

    return with_log, hists

def key_class(k):
    return getattr(R, k.GetClassName(), None)

def key_is_histogram(k):
    return issubclass(key_class(k), (R.TH1, R.THnSparse))

def get_hists_from_dir(d):
    """
    Return a dictionary {`name`: `histogram`} for all keys in TDirectory `d`
    """
    keys = list(d.GetListOfKeys())
    return dict((k.GetName(), k.ReadObj()) for k in keys if key_is_histogram(k))
    
def get_hists(*files):
    """
    Return the set of histograms in a directory called `d` which exists in both
    `f1` and `f2`
    """
    #h1s, h2s = get_hists_from_dir(f1.Get(d)), get_hists_from_dir(f2.Get(d))
    hists = [get_hists_from_dir(f) for f in files]
    histnames = [set(h) for h in hists]
    common_hists = reduce(set.__and__, histnames)
    return dict((hname, tuple(h[hname] for h in hists)) for hname in common_hists)

def ensure_dirs(*dirs):
    for d in dirs:
        if not isdir(d):
            assert not exists(d), "Trying to use file {0} as directory".format(d)
            makedirs(d)

TYPES = ["png", "eps"]
def save_canvas(c, d, name, with_log=False):
    ensure_dirs(*[pjoin(d, t) for t in TYPES])
    
    for t in TYPES:
        c.SaveAs(pjoin(d, t, name) + "." + t)
    
    if not with_log:
        return
    
    c.SetLogy()
    c.Update()
    for t in TYPES: c.SaveAs(pjoin(d, t, name) + ".log." + t)
    
def rescale(*hists):
    top = max(hist.GetMaximum() for hist in hists)
    bottom = min(hist.GetMinimum(1e-12) for hist in hists)
    for h in hists:
        h.GetYaxis().SetRangeUser(bottom*0.95, top*1.05)
    
def canvas_maintainer(seq):
    
    c = R.TCanvas()
    
    def generator(seq):
        for item in seq:
            c.Clear()
            c.SetLogy(False)
            
            dirname, hname, with_log, keep_alive = yield item
                        
            save_canvas(c, dirname, hname, with_log)
            
            for x in keep_alive:
                x.Delete()
                
            # Goes back to point at which send() was called
            yield

    gen = generator(seq)
    def send(*args): gen.send(args)
    return c, send, gen

def set_colors(hists, colors=(R.kRed, R.kGreen, R.kBlue)):
    for h, c in zip(hists, colors):
        h.SetLineColor(c)

def normalize(*hists):
    for h in hists:
        h.Scale(1. / h.Integral())
        h.GetYaxis().SetTitle("Normalized: arbitrary units")
    
def plot_barrel_endcap_histos(c, hname, h):
    
    # Eta bins:
    #  0., 0.60, 1.37, 1.52, 1.81, 2.37
    # Pt bins:
    #  15, 45, 60, 80, 120, 200, 400, 1000
    
    barrel = barrel_lo, barrel_hi = 1, 1 # (up to .6)
    endcap = endcap_lo, endcap_hi = 2, 6
    
    lopt = lopt_lo, lopt_hi = 0, 1 # (up to 45)
    hipt = hipt_lo, hipt_hi = 2, 8 # (up to >1000 GeV)
    
    pt_axis, eta_axis = h.GetYaxis(), h.GetZaxis()
    
    pt_axis.SetRange(*lopt); eta_axis.SetRange(*barrel); lopt_barrel = h.Project3D("x0")
    pt_axis.SetRange(*hipt); eta_axis.SetRange(*barrel); hipt_barrel = h.Project3D("x1")
    pt_axis.SetRange(*lopt); eta_axis.SetRange(*endcap); lopt_endcap = h.Project3D("x2")
    pt_axis.SetRange(*hipt); eta_axis.SetRange(*endcap); hipt_endcap = h.Project3D("x3")
    
    hists = lopt_barrel, hipt_barrel, lopt_endcap, hipt_endcap
    normalize(*hists)
    for h in hists:
        h.SetTitle("")
        h.SetStats(False)
        
        if "had" in hname:
            h.GetXaxis().SetRangeUser(-0.2, 0.2)
        
    c.Divide(2)
    
    c.cd(1)
    rescale(lopt_barrel, hipt_barrel)
    lopt_barrel.SetLineColor(R.kRed);  lopt_barrel.Draw("hist e0x0")
    hipt_barrel.SetLineColor(R.kBlue); hipt_barrel.Draw("hist e0x0 same")
    
    c.cd(2)
    rescale(lopt_endcap, hipt_endcap)
    lopt_endcap.SetLineColor(R.kRed);  lopt_endcap.Draw("hist e0x0")
    hipt_endcap.SetLineColor(R.kBlue); hipt_endcap.Draw("hist e0x0 same")
    
    return hists

def plot_dir_barrel_vs_endcap(dirname, d, in11):
    
    items = sorted(get_hists_from_dir(in11.Get(d)).iteritems())
    c, save_and_cleanup, items_cm = canvas_maintainer(items)
        
    for hname, h in items_cm:
        
        if h.GetDimension() != 3:
            continue
        
        with_log = False
        keep_alive = plot_barrel_endcap_histos(c, hname, h)
                
        save_and_cleanup(dirname, hname, with_log, keep_alive)

def make_plots_barrel_vs_endcap(what,  in11):
    plot_dir = plot_dir_barrel_vs_endcap
    
    plot_dir("{0}/all/pre_loose".format(what),        "all_{0}s/pre_loose".format(what),  in11)
    plot_dir("{0}/all/post_loose".format(what),       "all_{0}s/post_loose".format(what), in11)
    plot_dir("{0}/all/post_tight".format(what),       "all_{0}s/post_tight".format(what), in11)
    
    plot_dir("{0}/default/boson".format(what),        "default/{0}/boson".format(what),   in11)
    plot_dir("{0}/default/leading".format(what),      "default/{0}/1".format(what),       in11)
    plot_dir("{0}/default/subleading".format(what),   "default/{0}/2".format(what),       in11)
    
    if what == "ph":
        plot_dir("ph/corrected/boson",      "corrected/ph/boson", in11)
        plot_dir("ph/corrected/leading",    "corrected/ph/1",     in11)
        plot_dir("ph/corrected/subleading", "corrected/ph/2",     in11)    

def plot_dir_cut_progression(target_dir, what, in11):

    target_dir = target_dir.format(what)

    cuts = "pre_loose", "post_loose", "post_tight"
    dirs = [("all_{0}s/{1}".format(what, cut)) for cut in cuts]
    rdirs = map(in11.Get, dirs)
    items = sorted(get_hists(*rdirs).iteritems())
    
    c, save_and_cleanup, items_cm = canvas_maintainer(items)
    
    with_log = False
    
    for hname, hists in items_cm:
    
        if isinstance(hists[0], R.TH3):
            hists = [h.Project3D("x{0}".format(i)) for i, h in enumerate(hists)]
        elif isinstance(hists[0], R.TH2):
            c.Divide(len(hists))
            for i, h in enumerate(hists, 1):
                c.cd(i)
                h.Draw("colz")
            save_and_cleanup(target_dir, hname, with_log, hists)
            continue
        
        hists = map(fixup_hist_units, hists)
    
        with_log, hists = additional_processing(hname, hists)
    
        notloose, loose, tight = hists
        set_colors(hists)
        normalize(*hists)
        rescale(*hists)
        
        notloose.Draw("hist e0x0")
        loose.Draw("hist e0x0 same")
        tight.Draw("hist e0x0 same")
        
        save_and_cleanup(target_dir, hname, with_log, hists)

def make_plots_cut_progression(what, in11):
    plot_dir = plot_dir_cut_progression
    
    plot_dir("{0}/bycut", what, in11)

def main():
    R.gROOT.SetBatch()
    
    in11 = R.TFile.Open(input_2011)
    
    if False:
        make_plots_barrel_vs_endcap("ph", in11)
        make_plots_barrel_vs_endcap("el", in11)
    
        make_plots_cut_progression("ph", in11)
        make_plots_cut_progression("el", in11)
        
    make_plots_el_ph_compare(in11)
    
        
if __name__ == "__main__":
    main()
