#! /usr/bin/env python

from __future__ import division
from ROOT import TFile

from IPython.Shell import IPShellEmbed; ip = IPShellEmbed(["-pdb"]) 

from pprint import pprint
from numpy import array
import locale

def commas(i):
    import re
    orig = str(int(i)) if not isinstance(i, str) else i
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>,\g<2>', orig)
    if orig == new:
        return new
    else:
        return commas(new)
locale.setlocale(locale.LC_ALL, '') 

def dump_counts(f):

    labels = [f.cutflow.GetXaxis().GetBinLabel(i+1) for i in xrange(10)]
    labels = ("total", "grl", "vertex", "trigger", "nphot", "eta", "pt", 
              "oq", "jetclean", "loose", "tight")
    counts = ["%13s (%7.3f) : %s" % (commas(f.cutflow[1+i]), (100*f.cutflow[1+i] / f.cutflow[i]) if i else 100, s) for i, s in enumerate(labels)]
    values = [f.cutflow[1+i] for i in xrange(10)]
    print "\n".join(counts)
    return labels, array(values)
    
def main():
    
    period = "periodD-I"
    parts = ["periodD-I"] + list("DEFGHI")
    #parts = ["periodD-I"]
    for p in parts:
        if p != "periodD-I":
            period = "period-%s" % p
        fname = "/data1/pwaller/v15/passes/35/%s.root" % period
        print fname
        f15 = TFile(fname)
        labels, v15 = dump_counts(f15)
        fname = "/data1/pwaller/v16/passes/35/%s.root" % period
        print fname
        f16 = TFile(fname)
        labels, v16 = dump_counts(f16)
        
        print "Differences v16 - v15:"
        for label, diff in zip(labels, v16 - v15):
            print "%10s : %13s" % (label, commas(diff))
        print
        
        
        
    #f16 = TFile("/data1/pwaller/v16/passes/26/%s.root" % period)    
    #dump_counts(f16)
    
if __name__ == "__main__":
    main()
