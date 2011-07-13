import re
import ROOT as R

from cPickle import loads
from os import listdir, makedirs, rename
from os.path import basename, exists, join as pjoin

from commando import Application, command, subcommand, version, store, true, param

from yaml import load_all


from minty.metadata.lumicalc_parse import LumiInfo
from minty.utils.table_printer import pprint_table


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
    
    inputs = custom_sort(params.files)

    #inputs = [i for i in inputs if "PUNK" not in i and "periodP." not in i]
    
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
    
    assert len(labels) == 1, labels
    (labels,) = labels
    
    lumi = lambda f: []
    
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
                events = sum(d.totalevents for dd in ds for d in dd if d.period != "UNK")
            
            if isinstance(events, int):
                bad = "!" if events != h[1] else " "
            return [bad, events]
        extra_labels = ["?", "AMI events"]
        
        lumi = lambda f, h: []
        if exists("lumi.yaml"):
            extra_labels[:0] = ["lumi[1/pb]", "yield[per 1/pb]"]
            
            lumi_info = LumiInfo.from_file("lumi.yaml")
            lumi_by_run = lumi_info.total_per_run
            def lumi(f, h):
                name = basename(f)
                matchcounts = re.match("^.*?-P(.+)-R(\d+).root$", name)
                
                lumi = "-"
                if matchcounts:
                    period, run = matchcounts.groups()
                    lumi = lumi_by_run.get(int(run), 0)
                    
                elif name.startswith("period"):
                    period = name.split(".")[0][len("period"):]
                    if period in by_period:
                        lumi = sum(lumi_by_run[d.run] for d in by_period[period] 
                                   if d.run in lumi_by_run)
                    
                elif name.startswith("all"):
                    ds = [ds for name, ds in by_period.iteritems() if len(name) == 1]
                    lumi = sum(lumi_by_run[d.run] for dd in ds for d in dd 
                               if d.period != "UNK" and d.run in lumi_by_run)
                               
                def u_to_p(x): return x / 1e6
                lumi = u_to_p(lumi)
                
                if lumi:
                    final_count = h[h.GetNbinsX()]
                    from uncertainties import ufloat
                    from math import sqrt
                    final_count = ufloat((final_count, sqrt(final_count))) / lumi
                    args = final_count.nominal_value, final_count.std_dev()
                    final_count = "{0:6.2f}+-{1:6.2f}".format(*args)
                else:
                    final_count = "0"
                return ["{0:.2f}".format(lumi), final_count]
                
    else:
        def extra(f, h): return []
        extra_labels = []
    
    def pretty_file(f):
        if "all" in f:
            return "Total"
        f, _, ext = f.rpartition(".")
        if f.startswith("period"):
            return "period " + f[len("period"):]
        p, r = f.split("_")[-1].split("-")
        return "{0}:{1}".format(p, r.lstrip("R"))
    
        
    
    header = [["what"] + extra_labels + list(labels)]
    numbers = [[pretty_file(f)] + lumi(f, h) + extra(f, h) + map(int, get_bin_values(h)) 
               for f, h in zip([f.GetName() for f in files], cutflows)]
    table = header + numbers
    pprint_table(table)

@subcommand('kick', help="Remove datasets which aren't in the period")
@param('--dataset')
def kick(self, params):
    """
    Dump a list of datasets which need to be kicked
    """
    
    if not params.dataset:
        print "Please specify --datasets"
        raise SystemExit
    
    match = re.compile("^.*?-P(.+)-R(\d+).root$").match
    matches = ((f, match(f)) for f in listdir("."))
    files = [(name, f.groups()) for name, f in matches if f]
    files = sorted([(name, int(run), period.split("_")[-1]) for name, (period, run) in files])
    
    _, data_info = load_all(open(params.dataset))
    by_period, by_run = {}, {}
    for d in data_info["datasets"]:
        by_period.setdefault(d.period, []).append(d)
        by_period.setdefault(d.period[0], []).append(d)
        assert not d.run in by_run
        by_run[d.run] = d
           
        #by_run.setdefault(d.run, []).append(d)
        
    if not exists("kicked"):
        makedirs("kicked")
    
    for name, run, period in files:
        if period != by_run[run].period or period == "UNK":
            print name, period, by_run[run].period
            rename(name, pjoin("kicked", name))
            
    
@subcommand('dump_grl', help="Dump a grl from input datasets")
@param('-o', "--output", default="output.xml")
@param('files', nargs="+")
def dump_grl(self, params):
    from DQUtils import IOVSet
    
    total = IOVSet()
    for f in params.files:
        f = R.TFile.Open(f)
        grls = loads(f.file_metadata.GetString().Data())
        for grl in grls:
            grl = IOVSet.from_grl_string(grl)
            assert not grl & total
            total |= grl
    print total, "lumiblocks:", total.lb_counts
    total.to_grl(params.output)
    
@subcommand('dump_files', help="Dump list of files processed by a dataset")
@param('files', nargs="+")
def dump_files(self, params):
    for f in params.files:
        f = R.TFile.Open(f)
        file_list = loads(f.file_processed_list.GetString().Data())
        #print "\n".join(file_list)
        print type(file_list)

@subcommand('status', help='Dump basic information')
@param('files', nargs="+")
def status(self, params):
    inputs = custom_sort(params.files)

    from ROOT import TFile
    files = [TFile.Open(f) for f in inputs]
    
    def get_info(f):
        try:
            return [
                f.exception_count.GetVal(),
                f.cputime.GetVal(),
                f.skimtime.GetVal() if f.Get("skimtime") else "N/A",
                f.walltime.GetVal(),
                f.processed_trees.GetVal(),
                f.jobs_files.GetVal(),
            ]
        except AttributeError:
            return [None]*6
       
    labels = ["exceptions", "cputime", "skimtime", "walltime", "ntrees", "njf"]
    numbers = [[f.GetName()] + get_info(f) for f in files]
    table = [["file"] + list(labels)] + numbers
    pprint_table(table) 

@subcommand('mcupdateinfo', help='Update dataset info')
@param('files', nargs="*")
def mcupdateinfo(self, params):
    for filename in params.files:
        ds = PwaDataset.from_file(filename)
        for mcds in ds.datasets:
            mcds.mc_info
        ds.to_file(filename)

def save_ufloat(name, value):
    v = R.TParameter(float)("{0}_value".format(name), value.nominal_value)
    e = R.TParameter(float)("{0}_err".format(name), value.std_dev())
    v.Write()
    e.Write()
    
@subcommand('mcrescale', help="Scale datasets to montecarlo")
@param('-l', '--lumi', type=float, help="Luminosity")
@param('-u', '--uncert', default=None, type=float, help="Luminosity uncertainty percentage")
@param('files', nargs="*")
def mcrescale(self, params):
    from pwa.datasets import get_dataset_mapping
    from uncertainties import ufloat
    datasets = get_dataset_mapping("mc*")
    
    if not exists("pre_rescale"):
        makedirs("pre_rescale")
    
    match = re.compile("^.*?-P(.+)-R(\d+).root$").match
    lumi = params.lumi
    
    if params.uncert:
        lumi = ufloat((lumi, lumi * (params.uncert / 100.)))
    
    for filename in params.files:
        m = match(filename)
        if not m:
            print "Skipping", filename
            continue
        
        period, run = m.groups()
        dataset = datasets[int(run)]
        effective_lumi = dataset.effective_luminosity
        factor = dataset.reweight_factor(lumi)
        print "Processing", filename, period, run, dataset.physicsshort, effective_lumi, factor
        
        target_name = "mc_{d.run}_{d.physicsshort}.root".format(d=dataset)
        prerescale_path = pjoin("pre_rescale", filename)
        
        rename(filename, prerescale_path)
        f_in = R.TFile(prerescale_path, "read")
        f_out = R.TFile(target_name, "recreate")
        
        from minty.tools.minty_rescale import rescale_dir
        rescale_dir(f_in, f_out, factor.nominal_value)
        
        f_out.cd()
        save_ufloat("effective_lumi", effective_lumi)
        save_ufloat("mc_weight", factor)
