from optparse import OptionParser
from pprint import pprint
from os.path import basename

from pyfiglet import print_figlet

import minty

from minty.histograms.cuts_histogram import make_cut_histogram
from minty.utils import comma_num
from minty.utils.table_printer import pprint_table, compute_col_paddings

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
        ts = title.split("&")
        for t in ts:
            result.append(axes_dict[t])
            del axes_dict[t]
    for title, axis in axes_titles:
        if title in axes_dict:
            result.append(axis)
    return result    

def linkify(text):
    def thunk(pad, ljust):
        link = '<a href="#%s">%s</a>' % (text, text) 
        if len(text) < pad:
            padding = " " * (pad - len(text))
            if ljust:
                link = link + padding
            else:
                link = padding + link
        return link
    return thunk

def linkify_first_column(table_rows, options):
    if not options.htmlify:
        return table_rows
    table_columns = zip(*table_rows)
    first_column = [linkify(row) for row in table_columns[0]]
    table_rows = zip(*([first_column] + table_columns[1:]))
    return table_rows

def if_htmlify(func, options):
    return func if options.htmlify else (lambda s, *_: s)

def print_heading(text, options):
    if options.htmlify:
        print '<a name="%s"></a>' % text
    print "-"*80
    print_figlet(text)
    print text.center(80)
    print "-"*80

def do_cutflow_one_cut(total_hist, axis, cuts, options):
    if axis:
        title = aliases.get(axis.title, axis.title)
        prevno = axis.true
        cumulated_cuts = [axis.title]
    else:
        title = "all"
        #prevno = ph_cands.hist.GetEntries()
        a = total_hist.axes_objs[0]
        prevno = a.total
        cumulated_cuts = []
    
    row = [title, prevno]
    
    for cut in cuts:
        cut_parts = set(cut.split("&"))
        if axis:
            cut_parts.discard(axis.title)
            if not cut_parts:
                row.append("-")
                continue
        
        cumulated_cuts.extend(cut_parts)
        projax = total_hist(*cumulated_cuts)
        thisno = projax.true
        
        if options.percentage:
            perc = round(thisno / prevno * 100, 2) if prevno else 0
            row.append("%.2f" % perc)
        else:
            row.append(thisno)
            
        prevno = thisno
            
    return row

def do_cutflow_one_file(f, cuts, options):
    ph_cands = make_cut_histogram(f.photon_counts)
    #ph_cands = ph_cands.isConv.project_out(True)
    if options.apply_cut:
        cut, value = options.apply_cut.split(":")
        ph_cands = getattr(ph_cands, cut).project_out(int(value))
    
    rows = []
    for axis in [None] + ordered_axes(ph_cands.axes_objs, cuts):
        rows.append(do_cutflow_one_cut(ph_cands, axis, cuts, options))
        
    return rows

def do_cutflow(files, cuts, options):
    
    header = ["cut", "all"] + [aliases.get(a, a) for a in cuts]

    result = []

    for f in files:
        period = basename(f.GetName())
        table = do_cutflow_one_file(f, cuts, options)
        result.append((period, table))
        
    return result

def print_tables(firstpart, cuts, tables, options):
    _linkify = if_htmlify(linkify, options)
    
    aliased_cuts = [aliases.get(cut, cut) for cut in cuts]
    header = [firstpart, "all"] + aliased_cuts
    
    headings, _tables = zip(*tables)
    _tables += ([header],)
    col_paddings = compute_col_paddings(reduce(list.__add__, _tables, []))
    
    header = [firstpart, "all"] + map(_linkify, aliased_cuts)
    
    for heading, table in tables:
        print_heading(heading, options)
        table = linkify_first_column(table, options)
        pprint_table([header] + table, col_paddings=col_paddings)    

def do_by_cut(flow_result, cuts, options):
    
    result = []
    
    periods, tables = zip(*flow_result)
    table_rows_by_period = zip(*tables)
    for table_part in table_rows_by_period:
        columns = zip(*table_part)
        cut = columns[0][0]
        table = zip(*([periods] + columns[1:]))
    
        result.append((cut, table))
    
    return result            

def main():

    from IPython.Shell import IPShellEmbed; ip = IPShellEmbed(["-pdb"])

    parser = OptionParser()
    parser.add_option("-p", "--percentage", action="store_true", help="Show percentage change instead of absolute numbers")
    parser.add_option("-c", "--by-cut", action="store_true", help="Show by cut")
    parser.add_option("-H", "--htmlify", action="store_true", help="Use HTML")
    parser.add_option("-a", "--apply-cut", help="Apply a cut. Syntax: <cutname>:value")
    options, input_filenames = parser.parse_args()
    
    files = [R.TFile(filename) for filename in input_filenames]
    
    if options.htmlify:
        print "<pre>"
    #do_all(files)
    #cuts = "grl&oq&pv "
    cuts = "grl oq pv".split()
    
    cuts += "fiducial loose robust_nontight robust_tight pt_gt40 pt_gt100 isolated".split()
    result = do_cutflow(files, cuts, options)
    print_tables("cut", cuts, result, options)
    
    if options.by_cut:
        result = do_by_cut(result, cuts, options)
        print_tables("period", cuts, result, options)
        
    if options.htmlify:        
        print "</pre>"
            
    

