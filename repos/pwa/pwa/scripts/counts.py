from optparse import OptionParser
from pprint import pprint

import minty

from minty.histograms.cuts_histogram import make_cut_histogram
from minty.utils import comma_num
from minty.utils.table_printer import pprint_table

import ROOT as R

def do_all(files):
    for f in files:
        
        ph_cands = make_cut_histogram(f.photon_counts)
        events = make_cut_histogram(f.event_counts)
        
        #("oq", "grl", "pv", "pt_gt100").project_out().
        print filename
        print "\n".join("  %20s %12s %12s" % (a.title, comma_num(a.true), comma_num(a.total)) for a in ph_cands.axes_objs)

def do_cutflow_one_file(f, cuts):
    ph_cands = make_cut_histogram(f.photon_counts)
    
    rows = []
    for axis in ph_cands.axes_objs:
        row = [axis.title, axis.true]
        projax = axis.project_out()
        for cut in cuts:
            if cut == axis.title:
                row.append("-")
                continue
            projax = projax(cut)
            row.append(projax.true)
            projax = projax.project_out()
                
        rows.append(row)
    
    return rows

def do_cutflow(files, cuts):
    cuts = cuts.split()
    header = ["cut", "all"] + cuts

    for f in files:
        table = do_cutflow_one_file(f, cuts)
        pprint_table([header] + table)

def main():

    from IPython.Shell import IPShellEmbed; ip = IPShellEmbed(["-pdb"])

    parser = OptionParser()
    options, input_filenames = parser.parse_args()
    
    files = [R.TFile(filename) for filename in input_filenames]
    
    #do_all(files)
    do_cutflow(files, "isolated pt_gt100 oq pv grl loose robust_nontight robust_tight")
    

