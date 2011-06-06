import re

from os.path import basename

from commando import Application, command, subcommand, version, store, true, param

from yaml import load_all

def get_bin_values(h):
    xa = h.GetXaxis()
    return [h[i] for i in xrange(1, xa.GetNbins()+1)]

def mp_merge(args):
    from hmerge import merge_files
    merge_files(*args)

@subcommand('mergeall', help='Merge all of the files contained in a tgz')
@param('files', nargs="+")
def mergeall(self, params):
    from hmerge import merge_files
    from tarfile import open as tarfile_open
    from contextlib import closing
    
    print "Input:", params.files
    
    output_files = {}
    
    fileset = set()
    for f in params.files:
        with closing(tarfile_open(f)) as tar:
            for rootfile in tar.getmembers():
                output_files.setdefault(rootfile.path, set()).add(f)
    
    from multiprocessing import Pool
    pool = Pool(4)
    to_merge = [(output, sorted(inputs), output)
                for output, inputs in sorted(output_files.iteritems())]
    pool.map(mp_merge, to_merge)

@subcommand('reduce', help="Reduce many output- files to files by period.")
@store('-p', '--prefix', default="output-")
def reduce(self, params):
    from os import listdir
    files = [f for f in listdir(".") 
             if f.startswith(params.prefix) and f.endswith(".root")]
    
    def get_period(s): return s.split("-")[1].split("_")[-1]
    
    by_subperiod = {}
    for f in files:
        by_subperiod.setdefault(get_period(f), []).append(f)
        
    from pprint import pprint
    pprint(by_subperiod)
        
    from multiprocessing import Pool
    pool = Pool(4)
    
    pool.map(mp_merge, [("period%s.root" % p, files) for p, files in by_subperiod.iteritems()])
    
    by_period = {}
    for p, files in sorted(by_subperiod.iteritems()):
        by_period.setdefault(p[0], []).append("period%s.root" % p)
    
    pprint(by_period)
    
    pool.map(mp_merge, [("period%s.root" % p, files) for p, files in by_period.iteritems()])
    
    from hmerge import merge_files
    merge_files("all.root", ["period%s.root" % p for p in by_period])
    
    print "Done."

@subcommand('mergereduce', help="Run merge reduce")
@param('files', nargs="+")
@param("-p", "--prefix", default="output")
def mergereduce(self, params):
    mergeall(self, params)
    reduce(self, params)
    
def custom_sort(inputs):
    import re
    priorities = [
        lambda x: x == "all.root",
        lambda x: bool(re.match(r"period[A-Z]+\.root", x)),
        lambda x: bool(re.match(r"period[A-Z]+\d+\.root", x)),
    ]
    result = [[] for i in priorities] + [[]]
    for name in inputs:
        matched = False
        for i, matcher in enumerate(priorities):
            if matcher(name):
                matched = i
                break
        if matched is False:
            matched = len(priorities)
        result[matched].append(name)
    for r in result: r.sort()
    from itertools import chain
    return chain(*result)

@subcommand('dump', help='Dump basic information')
@param('files', nargs="+")
@param('--name', default="cutflow")
@param('--datasets')
def dump(self, params):
    from DQUtils.ext.table_printer import pprint_table
   
    inputs = custom_sort(params.files)

    from ROOT import TFile
    files = [TFile.Open(f) for f in inputs]
    good_files = []
    for f in files:
        if not f.Get(params.name):
            print "Warning, ignoring", f.GetName()
        else:
            good_files.append(f)
    files = good_files
    cutflows = [f.Get(params.name)  for f in files]
    axes = [c.GetXaxis() for c in cutflows]
    labels = set(tuple(a.GetBinLabel(i) for i in xrange(1, a.GetNbins()+1))
                 for a in axes)
    print labels
    assert len(labels) == 1, labels
    (labels,) = labels
    
    if params.datasets:
        _, data_info = load_all(open(params.datasets))
        by_period, by_run = {}, {}
        for d in data_info["datasets"]:
            by_period.setdefault(d.period, []).append(d)
            by_period.setdefault(d.period[0], []).append(d)
            by_run.setdefault(d.run, []).append(d)
            
        def extra(f, h):
            name = basename(f)
            bad, events = "-", "N/A"
            
            matchcounts = re.match("^.*?-P(.+)-R(\d+).root$", name)
            
            if matchcounts:
                period, run = matchcounts.groups()
                events = sum(d.totalevents for d in by_run[int(run)])
                
            elif name.startswith("period"):
                period = name.split(".")[0][len("period"):]
                if period in by_period:
                    events = sum(d.totalevents for d in by_period[period])
                    
            elif name.startswith("all"):
                ds = [ds for name, ds in by_period.iteritems() if len(name) == 1]
                events = sum(d.totalevents for dd in ds for d in dd)
            
            if isinstance(events, int):
                bad = "!" if events != h[1] else " "
            return [bad, events]
        extra_labels = ["?", "AMI events"]
    else:
        def extra(f, h): return []
        extra_labels = []
        
    numbers = [[f] + extra(f, h) + map(int, get_bin_values(h)) 
               for f, h in zip([f.GetName() for f in files], cutflows)]
    table = [["file"] + extra_labels + list(labels)] + numbers
    pprint_table(table)


@subcommand('status', help='Dump basic information')
@param('files', nargs="+")
def status(self, params):
    from DQUtils.ext.table_printer import pprint_table
    inputs = custom_sort(params.files)

    from ROOT import TFile
    files = [TFile.Open(f) for f in inputs]
    
    def get_info(f):
        return [
            f.exception_count.GetVal(),
            f.cputime.GetVal(),
            f.skimtime.GetVal() if f.Get("skimtime") else "N/A",
            f.walltime.GetVal(),
            f.processed_trees.GetVal(),
            f.jobs_files.GetVal(),
        ]
       
    labels = ["exceptions", "cputime", "skimtime", "walltime", "ntrees", "njf"]
    numbers = [[f.GetName()] + get_info(f) for f in files]
    table = [["file"] + list(labels)] + numbers
    pprint_table(table) 
    
