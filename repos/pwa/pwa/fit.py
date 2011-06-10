from __future__ import division

from array import array

import ROOT as R

from ROOT import TFile, gROOT, TCanvas

from subprocess import Popen, PIPE
from multiprocessing import Pool

from commando import subcommand, param

@subcommand('multifit', help='Draw plots')
@param('--dummy', '-d', action="store_true")
def multifit(self, params):
    import rootils.uncert as U
    from minty.utils import wait, canvas
    gROOT.SetBatch()
    R.gStyle.SetOptStat(1000000) # Integral only
    R.gStyle.SetOptFit(11)
    
    f = TFile("all.root")
    h = f.Get("corrected/ph/boson/mass_wide")
    
    window_size = 25
    
    bins = array('d', [])
    values = array('d', [])
    errors = array('d', [])
    
    for i in xrange(80, 600, 5):
        h.GetXaxis().SetRangeUser(i - window_size/2, i + window_size/2)
        
        with canvas() as c:
            const, slope = U.from_fitresultp(h.Fit("expo", "LLISQ"))
            c.SaveAs("plots/massfit-{0}GeV.png".format(i))
        
        integral = h.Integral()
        
        bins.append(i)
        values.append(slope.nominal_value)
        errors.append(slope.std_dev())
     
    gROOT.SetBatch(0)
    with canvas() as c:
        g = R.TGraphErrors(len(bins), bins, values, array('d', [0]*len(bins)), errors)
        g.Draw("A*P")
        c.SaveAs("plots/massfit-pieces.png")
        
        wait()
