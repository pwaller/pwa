#! /usr/bin/env python

from __future__ import division
from ROOT import TFile

from IPython.Shell import IPShellEmbed; ip = IPShellEmbed(["-pdb"]) 

from pprint import pprint


def dump_counts(f):

    labels = [f.cutflow.GetXaxis().GetBinLabel(i+1) for i in xrange(10)]
    counts = ["%9i (%5.1f) : %s" % (f.cutflow[1+i], (100*f.cutflow[1+i] / f.cutflow[i]) if i else 100, s) for i, s in enumerate(labels)]
    
    print "\n".join(counts)
    
def main():
    
    period = "all"
    
    for p in ["all"] + list("DEFGHI"):
        if p != "all":
            period = "period-%s" % p
        fname = "/data1/pwaller/v15/passes/32/%s.root" % period
        print fname
        f15 = TFile(fname)
        dump_counts(f15)
        #fname = "/data1/pwaller/v16/passes/30/%s.root" % period
        #print fname
        #f16 = TFile(fname)
        #dump_counts(f16)
        
    #f16 = TFile("/data1/pwaller/v16/passes/26/%s.root" % period)    
    #dump_counts(f16)
    
if __name__ == "__main__":
    main()
