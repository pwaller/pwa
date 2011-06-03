#! /usr/bin/env python

from minty.base import AnalysisBase
from minty.main import make_main
from math import cosh


CUTFLOW = "named", "total", "vertex", ">2ph", ">2el", "passed", "1g1e"
(                   TOTAL,   VERTEX,   GT2PH,  GT2EL,   PASSED,  OGOE) = range(len(CUTFLOW)-1)

def do_skim(ana, event):
    counts = ana.h.get("cutflow", b=[CUTFLOW])

    counts(TOTAL)
    
    if not any(v.nTracks >= 3 for v in event.vertices): return
    counts(VERTEX)
    
    good_phs = [ph for ph in event.photons
                if ph.cl.E / cosh(ph.etas2) > 25000 and
                   abs(ph.etas2) < 1.37 or 1.52 < abs(ph.etas2) < 2.37 and
                   ph.loose and
                   not (ph.OQ & 34214)]
    
    if len(good_phs) >= 2: counts(GT2PH)
    
    # Hit dependent pt = cl_E / cosh(track eta) if >= 4 tracks else cl_pt
    good_els = [el for el in event.electrons
                if el.author not in (1, 3) and
                   el.hit_dependent_pt > 25000 and
                   abs(el.etas2) < 1.37 or 1.52 < abs(el.etas2) < 2.37 and
                   el.loose and
                   not (el.OQ & 34214)]
                   
    if len(good_els) >= 2: counts(GT2EL)
                   
    if len(good_phs) + len(good_els) >= 2:
        counts(PASSED)
        # Magic flag causes events to be dumped later.
        ana.should_dump = True
        
        if not sum(1 for p in good_phs if p.ambiguity_resolved) >= 2 and not len(good_els) >= 2:
            # We only have one AR photon and one electron.
            counts(OGOE)
    
class GravitonSkim(AnalysisBase):
    def __init__(self, tree, options):
        super(GravitonSkim, self).__init__(tree, options)
        
        self.tasks.extend([
            do_skim,
        ])

graviton_skim = make_main(GravitonSkim)
if __name__ == "__main__":
    graviton_skim()
