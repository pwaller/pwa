#! /usr/bin/env python

from commands import getstatusoutput
from pkg_resources import resource_listdir, resource_filename
from pprint import pprint
from subprocess import Popen, PIPE

from commando import Application, command, subcommand, version, store, true, param

from yaml import load_all, dump_all

user = "PeterWaller"

@subcommand('make_datasets', help='Build a new dataset')
@param('files', nargs="+")
def make_datasets(self, params):
    #print "Here..", params
    
    for f in params.files:
        items = load_all(f)

def list_datasets():
    def ds_filename(x):
        return resource_filename("pwa.datasets", x)
    def ds_name(x):
        return x.rpartition(".")[0]
    def ds_load(x):
        ds = ds_name(x)
        with open(ds_filename(x)) as fd:
            ds_info, ds_datasets = list(load_all(fd))
            ds_info["container_name"] = ds_info["container"].format(
                user=user, dsname=ds, **ds_info)
            return ds_info, ds_datasets 
            
    return [(ds_name(x), ds_filename(x), ds_load(x))
            for x in resource_listdir("pwa", "datasets") 
            if x.endswith(".yaml")]

@subcommand('dsupdate', help='Update dataset info')
@param('-d')
def dsupdate(self, params):

    for ds, ds_filename, (ds_info, ds_datasets) in list_datasets():

        if "pattern" not in ds_info:
            continue
        
        print ds_filename
        print ds_info
        
        ds_info["version"] = ds_info.get("version", 0) + 1
        
        datasets = dq2_ls(ds_info["pattern"])
        expanded = dq2_expand_containers(datasets)
        
        with open(ds_filename, "w") as fd:
            ds_datasets = dict(datasets=datasets, datasets_expanded=expanded)
            fd.write(dump_all([ds_info, ds_datasets]))
            
@subcommand('dsbuild', help='Update dataset info')
@param('-d')
def dsbuild(self, params):
    for ds, ds_filename, (ds_info, ds_datasets) in list_datasets():
        cont = ds_info["container_name"]
        x = dq2_ls(cont)
        if x:
            print "Skipping", ds, "- it already exists. Bump the version number"
            continue
        dq2_register_container(cont, ds_datasets["datasets_expanded"])        

def dq2_register_container(container_name, datasets):
    cmd = "dq2-register-container {0}".format(container_name)
    status, output = getstatusoutput(cmd)
    assert not status, "Failed: {0}".format(output)
    
    p = Popen(["xargs", "dq2-register-datasets-container", container_name], 
              stdin=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate("\n".join(datasets))
    result = p.wait()
    print stdout, stderr
    print "Done:", container_name, result
    

def dq2_expand_containers(cs):
    p = Popen(["xargs", "-P4", "-n1", "dq2-list-datasets-container"], 
              stdin=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate("\n".join(cs))
    p.wait()
    return sorted([x for x in stdout.split("\n") if x])
        
def dq2_ls(pattern):
    status, output = getstatusoutput("dq2-ls {0}".format(pattern))
    assert not status, "Failed: {0}".format(output)
    return sorted([x for x in output.strip().split("\n") if x])

def filter_valid_runs(dsnames, valid_runs):
    return [d for d in dsnames if dataset_run(d) in valid_runs]

def dataset_run(dsname):
    return int(dsname.split(".")[1])

def max_tag_per_run(datasets):
    ds={}
    for line in (l for l in datasets if l.strip()):
        ds.setdefault(dataset_run(line), []).append(line.strip())
            
    return [max(datasets) for run, datasets in sorted(ds.iteritems())]
