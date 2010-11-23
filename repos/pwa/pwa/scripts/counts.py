from optparse import OptionParser
from pprint import pprint
from os.path import basename

import minty

from minty.histograms.cuts_histogram import make_cut_histogram
from minty.utils import comma_num
from minty.utils.table_printer import pprint_table

import ROOT as R

aliases = dict(
    high_pt="pt_gt40",
)

def do_all(files):
    for f in files:
        
        ph_cands = make_cut_histogram(f.photon_counts)
        events = make_cut_histogram(f.event_counts)
        
        #("oq", "grl", "pv", "pt_gt100").project_out().
        print filename
        print "\n".join("  %20s %12s %12s" % (a.title, comma_num(a.true), comma_num(a.total)) for a in ph_cands.axes_objs)

def ordered_axes(axes, ordering):
    axes_titles = [(a.title, a) for a in axes]
    axes_dict = dict(axes_titles)
    result = []
    for title in ordering:
        result.append(axes_dict[title])
        del axes_dict[title]
    for title, axis in axes_titles:
        if title in axes_dict:
            result.append(axis)
    return result    

def do_cutflow_one_file(f, cuts):
    ph_cands = make_cut_histogram(f.photon_counts)
    projax = ph_cands
    
    rows = []
    for axis in [None] + ordered_axes(ph_cands.axes_objs, cuts):
        if axis:
            title = aliases.get(axis.title, axis.title)
            prevno = axis.true
            projax = axis.project_out()
        else:
            title = "all"
            prevno = ph_cands.hist.GetEntries()
        row = [title, prevno]
            
        for cut in cuts:
            if axis and cut == axis.title:
                row.append("-")
                continue
            projax = projax(cut)
            thisno = projax.true
            #row.append("%.2f" % round(thisno / prevno * 100, 2) if prevno else 0)
            row.append(thisno)
            prevno = thisno
            projax = projax.project_out()
                
        rows.append(row)
    
    return rows

def do_cutflow(files, cuts):
    cuts = cuts.split()
    header = ["cut", "all"] + [aliases.get(a, a) for a in cuts]

    import pyfiglet
    fig = pyfiglet.Figlet("/usr/share/figlet", font="standard", justify="center")

    for f in files:
        period = basename(f.GetName())
        print "-"*80
        print fig.renderText(period)
        print period.center(80)
        print "-"*80
        table = do_cutflow_one_file(f, cuts)
        pprint_table([header] + table)

def main():

    from IPython.Shell import IPShellEmbed; ip = IPShellEmbed(["-pdb"])

    parser = OptionParser()
    options, input_filenames = parser.parse_args()
    
    files = [R.TFile(filename) for filename in input_filenames]
    
    #do_all(files)
    do_cutflow(files, "grl oq pv isolated loose robust_nontight robust_tight high_pt pt_gt100")
    

