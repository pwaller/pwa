#! /usr/bin/env python

from __future__ import division
from ROOT import TFile

from IPython.Shell import IPShellEmbed; ip = IPShellEmbed(["-pdb"]) 

from pprint import pprint
from numpy import array

def dump_counts(f):

    labels = [f.cutflow.GetXaxis().GetBinLabel(i+1) for i in xrange(10)]
    counts = ["%9i (%5.1f) : %s" % (f.cutflow[1+i], (100*f.cutflow[1+i] / f.cutflow[i]) if i else 100, s) for i, s in enumerate(labels)]
    values = [f.cutflow[1+i] for i in xrange(10)]
    print "\n".join(counts)
    return labels, array(values)
    
def main():
    
    period = "all"
    parts = ["all"] + list("DEFGHI")
    #parts = ["all"]
    for p in parts:
        if p != "all":
            period = "period-%s" % p
        fname = "/data1/pwaller/v15/passes/32/%s.root" % period
        print fname
        f15 = TFile(fname)
        labels, v15 = dump_counts(f15)
        fname = "/data1/pwaller/v16/passes/32/%s.root" % period
        print fname
        f16 = TFile(fname)
        labels, v16 = dump_counts(f16)
        
        pprint(zip(labels, v16 - v15))
        
        
        
    #f16 = TFile("/data1/pwaller/v16/passes/26/%s.root" % period)    
    #dump_counts(f16)
    
if __name__ == "__main__":
    main()
