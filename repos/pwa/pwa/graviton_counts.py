#! /usr/bin/env python

from math import cosh, sqrt

from ROOT import gRandom, TNtuple

from minty.base import AnalysisBase
from minty.histograms import double_bins, mirror_bins, scale_bins
from minty.main import make_main
from minty.treedefs.egamma import Photon, Electron
           
def pairs_with_sum(inputs):
    if len(inputs) < 2:
        return
    for i, o1 in enumerate(inputs):
        for o2 in inputs[i+1:]:
            yield o1+o2, (o1, o2)
    
def counts(ana, event):
    counts = ana.h.get("cutflow", b=[(9, 0, 9)])
    
    # Total
    counts(0)
    
    # Pass Trigger
    if event.RunNumber < 160889:
        trigger = any(ph.L1_e > 14 for ph in event.photons)
        #event.L1.EM14
    else:
        trigger = event.EF._2g15_loose
    
    if not trigger: return
    counts(1)
    
    # Pass GRL
    if not event.is_grl: return
    counts(2)
    
    # Pass vertex
    # Requirement for other paper: and v.zvertex < 150. 
    if not any(v.nTracks >= 3 for v in event.vertices):
        return
    counts(3)
    
    good_photons = event.photons
    
    if len(good_photons) < 2: return
    counts(4)
    
    # Pass nphot
    good_photons = [ph for ph in good_photons if ph.pass_fiducial]
    if len(good_photons) < 2: return
    counts(5)
    
    # Pass object quality
    good_photons = [ph for ph in good_photons if ph.good_oq]
    if len(good_photons) < 2: return
    counts(6)
    
    # Pass jet cleaning
    good_photons = [ph for ph in good_photons if ph.good_jet_quality]
    
    if len(good_photons) < 2: return
    counts(7)

    # Pass looseness
    good_photons = [ph for ph in good_photons if ph.loose]
    if len(good_photons) < 2: return
    counts(8)
    
    # Pass tightness
    if sum(1 for ph in good_photons if ph.robust_tight) >= 2:
        counts(9)
    
    ph1, ph2 = good_photons[:2]
    
    comb = ph1 + ph2
    #print comb.m
    
    ana.h.get("mass", b=[(100, 100, 500)])(comb.m/1000)
    
class GravitonAnalysis(AnalysisBase):
    def __init__(self, tree, options):
    
        super(GravitonAnalysis, self).__init__(tree, options)
        
        # Tasks to run in order
        self.tasks.extend([
            counts,
        ])

    def finalize(self):
    
        super(GravitonAnalysis, self).finalize()

graviton_main = make_main(GravitonAnalysis)    
if __name__ == "__main__":
    graviton_main()
