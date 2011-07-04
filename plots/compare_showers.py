#! /usr/bin/env python

from os import makedirs
from os.path import exists, isdir, join as pjoin

import ROOT as R
from minty.histograms import fixup_hist_units

input_2011 = "../results/51/all.root"

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
    
def get_hists(d, f1, f2):
    """
    Return the set of histograms in a directory called `d` which exists in both
    `f1` and `f2`
    """
    h1s, h2s = get_hists_from_dir(f1.Get(d)), get_hists_from_dir(f2.Get(d))
    return [(h, h1s[h], h2s[h]) for h in set(h1s) & set(h2s)]

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

def compare_h1(h1, h2):
    h1.SetStats(False); h1.SetTitle("")
    h2.SetStats(False); h2.SetTitle("")
    
    h1 = fixup_hist_units(h1)
    h2 = fixup_hist_units(h2)
    
    h1.Scale(h2.Integral() / h1.Integral())
    
    h1.SetLineColor(R.kBlue)
    h2.SetLineColor(R.kRed)
    
    h2.Draw()
    h1.Draw("same")
    return h1, h2
    
def rescale(*hists):
    top = max(hist.GetMaximum() for hist in hists)
    for h in hists:
        h.GetYaxis().SetRangeUser(1e-12, top*1.05)
    
def plot_histo(c, hname, h):
    
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
    for h in hists:
        h.SetTitle("")
        h.SetStats(False)
        h.Scale(1. / h.Integral())
        h.GetYaxis().SetTitle("Normalized: arbitrary units")
        
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
    
def plot_dir(dirname, d, in11):
    
    c = R.TCanvas()
        
    for hname, h in sorted(get_hists_from_dir(in11.Get(d)).iteritems()):
        c.Clear()
        c.SetLogy(False)
        
        if h.GetDimension() != 3:
            continue
        
        with_log = False
        keep_alive = plot_histo(c, hname, h)
                
        save_canvas(c, dirname, hname, with_log)
        
        for x in keep_alive:
            x.Delete()

def make_plots(what,  in11):
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

def main():
    R.gROOT.SetBatch()
    
    in11 = R.TFile.Open(input_2011)
    make_plots("ph", in11)
    make_plots("el", in11)
        
if __name__ == "__main__":
    main()
