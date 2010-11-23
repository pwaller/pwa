from optparse import OptionParser
from pprint import pprint
from os.path import basename

import minty

from minty.histograms.cuts_histogram import make_cut_histogram
from minty.utils import comma_num
from minty.utils.table_printer import pprint_table

import ROOT as R


import pyfiglet
fig = pyfiglet.Figlet("/usr/share/figlet", font="standard", justify="center")

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

def link_targetify(text, center=False):
    return '<a name="%s"></a>%s' % (text, text.center(80) if center else text)

def linkify(text):
    return '<a href="#%s">%s</a>' % (text, text)

def print_heading(text):
    print "-"*80
    print fig.renderText(text)
    print link_targetify(text, True)
    print "-"*80
    

def do_cutflow_one_file(f, cuts, options):
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
            if options.percentage:
                row.append("%.2f" % round(thisno / prevno * 100, 2) if prevno else 0)
            else:
                row.append(thisno)
            prevno = thisno
            projax = projax.project_out()
                
        rows.append(row)
    
    return rows

def do_cutflow(files, cuts, options):
    header = ["cut", "all"] + [aliases.get(a, a) for a in cuts]

    result = []

    for f in files:
        period = basename(f.GetName())
        print_heading(period)
        table = do_cutflow_one_file(f, cuts, options)
        result.append((period, table))
        pprint_table([header] + table)
        
    return result

def do_by_cut(flow_result, cuts, options):
    header = ["period", "all"] + [aliases.get(a, a) for a in cuts]
    
    periods, tables = zip(*flow_result)
    periods = ["period %s" % period.split(".")[0][-1] for period in periods]
    table_rows_by_period = zip(*tables)
    for table_part in table_rows_by_period:
        columns = zip(*table_part)
        cut = columns[0][0]
        columns = zip(*([periods] + columns[1:]))
        print_heading(cut)
        pprint_table([header] + columns)
        
        #for period, part in zip(periods, columns):
            

def main():

    from IPython.Shell import IPShellEmbed; ip = IPShellEmbed(["-pdb"])

    parser = OptionParser()
    parser.add_option("-p", "--percentage", action="store_true", help="Show percentage change instead of absolute numbers")
    parser.add_option("-c", "--by-cut", action="store_true", help="Show by cut")
    options, input_filenames = parser.parse_args()
    
    files = [R.TFile(filename) for filename in input_filenames]
    
    print "<pre>"
    #do_all(files)
    cuts = "grl oq pv loose robust_nontight robust_tight high_pt pt_gt100".split()
    result = do_cutflow(files, cuts, options)
    do_by_cut(result, cuts, options)
    print "</pre>"
            
    

