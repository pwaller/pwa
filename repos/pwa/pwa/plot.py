import ROOT as R

from ROOT import TFile, gROOT, TCanvas

from subprocess import Popen, PIPE
from multiprocessing import Pool

from commando import subcommand, param

def make_uncertainty_funcs(fitresultp, fn):
    fitresult = fitresultp.Get()
    errd, erru = fitresult.LowerError(1), fitresult.UpperError(1)
    fnd, fnu = fn.Clone(fn.GetName() + "_down"), fn.Clone(fn.GetName() + "_up")
    fnd.SetLineColor(R.kRed); fnd.SetLineStyle(2)
    fnd.SetParameter(1, fnd.GetParameter(1) - errd)
    fnu.SetLineColor(R.kRed); fnu.SetLineStyle(2)
    fnu.SetParameter(1, fnu.GetParameter(1) + erru)
    return fnd, fnu

def plot_uncorrected_mass(f, lo, hi):
    f = TFile(f)
    c = TCanvas()
    h = f.Get("default/ph/boson/mass_wide")
    h = h.Rebin(4)
    h.GetXaxis().SetRangeUser(lo, hi)
    h.GetYaxis().SetTitle("N / (%.2f GeV)" % h.GetXaxis().GetBinWidth(1))
    h.GetYaxis().SetTitleOffset(1.25)
    fitresultp = h.Fit("expo", "LLIS")
    
    print list(c.GetListOfPrimitives())
    fn = h.GetListOfFunctions()[0]
    fn.SetLineWidth(1); fn.SetLineColor(R.kBlue)
    
    fnd, fnu = make_uncertainty_funcs(fitresultp, fn)

    h.SetTitle("uncorrected/ph/boson/mass")
    h.Draw()
    fnd.Draw("same")
    fnu.Draw("same")
    c.SaveAs("plots/mass_wide_{0}-{1}.png".format(lo, hi))

@subcommand('draw', help='Draw plots')
@param('files', nargs='+')
#@param('what'
def draw(self, params):
    
    gROOT.SetStyle("Plain")
    gROOT.SetBatch()
    
    results = []
    def do(func, *args):
        results.append(p.apply_async(func, args))
    
    for f in params.files:
        # = TFile(f)
        p = Pool(4)
        
        do(plot_uncorrected_mass, f, 100, 200)
        do(plot_uncorrected_mass, f, 100, 500)
        do(plot_uncorrected_mass, f, 300, 500)
        do(plot_uncorrected_mass, f, 300, 1000)
        do(plot_uncorrected_mass, f, 750, 1000)

        for r in results:
            r.get()
    
    
