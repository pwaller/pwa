#! /usr/bin/env python

from os import makedirs
from os.path import exists, isdir, join as pjoin

import ROOT as R
from minty.histograms import fixup_hist_units

input_2010 = "../results/43/d10/all.root"
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

def additional_processing(hname, h1, h2):
    with_log = False
    if "mass" in hname:
        h1 = h1.Rebin(10); h2 = h2.Rebin(10)
        with_log = True
        
    elif "cone" in hname:
        with_log = True
        
    elif ("pt" in hname or hname in ["E", "et"]) and (not "_vs" in hname and not "cone" in hname):
        if not h1.GetXaxis().IsVariableBinSize():
            h1 = h1.Rebin(5); h2 = h2.Rebin(5)
            if "wide" in hname:
                h1 = h1.Rebin(2); h2 = h2.Rebin(2)
        with_log = True

    elif "had" in hname:
        h1.GetXaxis().SetRangeUser(-0.2, 0.2)
        h2.GetXaxis().SetRangeUser(-0.2, 0.2)

    return with_log, h1, h2

def plot_dir(dirname, d, in10, in11):
    
    c = R.TCanvas()
        
    for hname, h1, h2 in get_hists(d, in10, in11):
        print "Plotting", hname
        c.Clear()
        c.SetLogy(False)
        
        with_log, h1, h2 = additional_processing(hname, h1, h2)
        
        if h1.GetDimension() == 3:
            print "<-- projecting"
            h1x, h2x = h1.Project3D("x1"), h2.Project3D("x2")
            print "--> projecting"
            h1x, h2x = compare_h1(h1x, h2x)
        
        elif h1.GetDimension() == 2:
            c.Divide(2)
            c.cd(1); h1.Draw("colz")
            c.cd(2); h2.Draw("colz")
            
        else:
            h1, h2 = compare_h1(h1, h2)
        
        save_canvas(c, dirname, hname, with_log)

def compare_obj(what, in10, in11):
    plot_dir("{0}/all/pre_loose".format(what),        "all_{0}s/pre_loose".format(what),    in10, in11)
    plot_dir("{0}/all/post_loose".format(what),       "all_{0}s/post_loose".format(what),   in10, in11)
    plot_dir("{0}/all/post_tight".format(what),       "all_{0}s/post_tight".format(what),   in10, in11)
    
    plot_dir("{0}/default/boson".format(what),        "default/{0}/boson".format(what),     in10, in11)
    plot_dir("{0}/default/leading".format(what),      "default/{0}/1".format(what),         in10, in11)
    plot_dir("{0}/default/subleading".format(what),   "default/{0}/2".format(what),         in10, in11)
    
    if what == "ph":
        plot_dir("ph/corrected/boson",      "corrected/ph/boson",   in10, in11)
        plot_dir("ph/corrected/leading",    "corrected/ph/1",       in10, in11)
        plot_dir("ph/corrected/subleading", "corrected/ph/2",       in10, in11)

def main():
    R.gROOT.SetBatch()
    
    in10, in11 = R.TFile.Open(input_2010), R.TFile.Open(input_2011)
    
    compare_obj("ph", in10, in11)
    compare_obj("el", in10, in11)
    
if __name__ == "__main__":
    main()
