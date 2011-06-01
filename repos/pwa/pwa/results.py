from commando import Application, command, subcommand, version, store, true, param

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
@store('-d', '--dummy')
def reduce(self, params):
    from os import listdir
    files = [f for f in listdir(".") 
             if f.startswith("output-") and f.endswith(".root")]
    
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
def mergereduce(self, params):
    mergeall(self, params)
    reduce(self, params)

@subcommand('dump', help='Dump basic information')
@param('files', nargs="+")
def dump(self, params):
    from DQUtils.ext.table_printer import pprint_table

    from ROOT import TFile
    files = [TFile.Open(f) for f in params.files]
    good_files = []
    for f in files:
        if not f.cutflow:
            print "Warning, ignoring", f.GetName()
        else:
            good_files.append(f)
    files = good_files
    cutflows = [f.cutflow for f in files]
    axes = [c.GetXaxis() for c in cutflows]
    labels = set(tuple(a.GetBinLabel(i) for i in xrange(1, a.GetNbins()+1))
                 for a in axes)
    assert len(labels) == 1
    (labels,) = labels
    numbers = [[f] + map(int, get_bin_values(h)) 
               for f, h in zip([f.GetName() for f in files], cutflows)]
    table = [["file"] + list(labels)] + numbers
    from pprint import pprint
    #pprint(table)
    pprint_table(table)
