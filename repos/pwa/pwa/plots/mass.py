from minty.utils import wait
from minty.histograms import meaningful_yaxis

from ROOT import gStyle
import ROOT as R

def draw_conversions(directory):
    from minty.utils.brace_expand import get_expand
    #gStyle.SetOptStat(1110)
    gStyle.SetOptStat(11111111)
    variable = "eta"
    variable = "mass_wide"
    #variable = "deltar"
    hists = get_expand(directory, "conv{1,2,neither,both}/boson/%s" % variable)
    hists = map(meaningful_yaxis, hists)
    conv1, conv2, convn, convb = hists
    
    titles = ["(only) Leading converted", 
              "(only) Subleading converted", 
              "Neither converted", 
              "Both converted"]
    
    
    
    for h, t in zip(hists, titles):
        
        h.SetTitle(t)
        #if variable in ["mass_wide", "phi"]:
        #print "Scaling", h
        #h.Scale(convn.Integral() / h.Integral())
        
        if variable == "mass_wide":
            h.Rebin(4000 / 2000) # (4000 is original binning, 200 target)
            h.GetXaxis().SetRangeUser(50, 200)
            h.GetXaxis().SetRangeUser(80, 100)
        if variable == "eta":
            h.Rebin(2)
    
    maxv = max(h.GetMaximum() * 1.1 for h in hists)
    for h in hists:
        h.GetYaxis().SetRangeUser(0, maxv)
    
    canvas = R.TCanvas("mass-conversions", "Mgg conversions")
    canvas.Divide(2,2)
    #strs = canvas.strs = []
    for i, h in enumerate(hists):
        canvas.cd(i+1)
        h.Draw()
        convn.SetLineColor(R.kRed)
        convn.Draw("same hist")
        
        #t = R.TText(0.4, 0.5, h.GetTitle())
        #t.SetNDC()
        #strs.append(t)
        #t.Draw()
        
    
    wait()
    if canvas:
        canvas.Close()
        
