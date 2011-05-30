#! /usr/bin/env python

from commands import getstatusoutput
from pkg_resources import resource_listdir, resource_filename
from pprint import pprint
from subprocess import Popen, PIPE

from commando import Application, command, subcommand, version, store, true, param

from yaml import load_all, dump_all

@subcommand('make_datasets', help='Build a new dataset')
@param('files', nargs="+")
def make_datasets(self, params):
    #print "Here..", params
    
    for f in params.files:
        items = load_all(f)

@subcommand('dsupdate', help='Update dataset info')
@param('-d')
def dsupdate(self, params):
    #from DQUtils.periods import fetch_project_period_runs
    #project_period_runs = fetch_project_period_runs()
    #valid_runs = set(r for proj, pers in project_period_runs.iteritems()
                     #for per, runs in pers.iteritems()
                     #for r in runs)
    #print len(valid_runs)
    

    for ds in [x for x in resource_listdir("pwa", "datasets") 
               if x.endswith(".yaml")]:
        ds_filename = resource_filename("pwa.datasets", ds)
        with open(ds_filename) as fd:
            ds_info, ds_datasets = list(load_all(fd))

        if "pattern" not in ds_info:
            continue
        
        print ds_filename
        print ds_info
        
        ds_info["version"] = ds_info.get("version", 0) + 1
        
        datasets = dq2_ls(ds_info["pattern"])
        expanded = dq2_expand_containers(datasets)
        
        with open(ds_filename, "w"):
            ds_datasets = dict(datasets=datasets, datasets_expanded=expanded)
            dump_all([ds_info, ds_datasets])

def dq2_expand_containers(cs):
    p = Popen(["xargs", "-P4", "-n1", "dq2-list-datasets-container"], stdin=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate("\n".join(cs))
    p.wait()
    return sorted([x for x in stdout.split("\n") if x])
        
def dq2_ls(pattern):
    status, output = getstatusoutput("dq2-ls {0}".format(pattern))
    assert not status, "Failed: {0}".format(output)
    return sorted(output.strip().split("\n"))

def filter_valid_runs(dsnames, valid_runs):
    return [d for d in dsnames if dataset_run(d) in valid_runs]

def dataset_run(dsname):
    return int(dsname.split(".")[1])

def max_tag_per_run(datasets):
    ds={}
    for line in (l for l in datasets if l.strip()):
        ds.setdefault(dataset_run(line), []).append(line.strip())
            
    return [max(datasets) for run, datasets in sorted(ds.iteritems())]
