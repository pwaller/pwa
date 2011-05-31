#! /usr/bin/env python

from commands import getstatusoutput
from os.path import abspath
from pkg_resources import resource_listdir, resource_filename
from pprint import pprint
from subprocess import Popen, PIPE

from commando import Application, command, subcommand, version, store, true, param

from yaml import load_all, dump_all

from minty.metadata.ami import query_datasets

user = "PeterWaller"

@subcommand('make_datasets', help='Build a new dataset')
@param('files', nargs="+")
def make_datasets(self, params):
    #print "Here..", params
    
    for f in params.files:
        items = load_all(f)

def ds_containername(x):
    cn = x["container_name"] = x["container"].format(user=user, dsname=x["shortname"], **x)
    return cn
def ds_filename(x):
    return resource_filename("pwa.datasets", x)
def ds_name(x):
    return x.rpartition(".")[0]
def ds_load(x):
    ds = ds_name(x)
    with open(ds_filename(x)) as fd:
        ds_info, ds_datasets = list(load_all(fd))
        ds_info["shortname"] = x.rpartition(".")[0]
        ds_info["container_name"] = ds_containername(ds_info)
        return ds_info, ds_datasets
        
def list_datasets():
            
    return [(ds_name(x), ds_filename(x), ds_load(x))
            for x in resource_listdir("pwa", "datasets") 
            if x.endswith(".yaml")]

@subcommand('dsupdate', help='Update dataset info')
@param('files', nargs="*")
def dsupdate(self, params):
    fileset = set(abspath(p) for p in params.files)
    
    from IPython.Shell import IPShellEmbed
    ip = IPShellEmbed(["-pdb"])

    for ds, ds_filename, (ds_info, ds_datasets) in list_datasets():
        if fileset and ds_filename not in fileset:
            continue

        if "pattern" not in ds_info:
            continue
        
        print "Updating dataset:", ds_filename
        
        # Find datasets matching pattern (which are VALID and EVENTS_AVAILABLE)
        datasets = query_datasets(ds_info["pattern"])
        if not datasets:
            # Fallback to dq2-ls
            log.warning("Couldn't find dataset for pattern %s" % ds_info["pattern"])
            log.warning("on AMI. Falling back to dq2-ls.")
            datasets = dq2_ls(ds_info["pattern"])
            
        # Expand containers
        expanded = dq2_expand_containers([d.name for d in datasets])
        
        with open(ds_filename, "w") as fd:
            ds_datasets = dict(datasets=datasets, datasets_expanded=expanded)
            fd.write(dump_all([ds_info, ds_datasets], default_flow_style=False))
            
@subcommand('dsbuild', help='Update dataset info')
@param('files', nargs="*")
def dsbuild(self, params):
    fileset = set(abspath(p) for p in params.files)
    
    for ds, ds_filename, (ds_info, ds_datasets) in list_datasets():
        if fileset and ds_filename not in fileset:
            continue
        
        ds_info["version"] = ds_info.get("version", 0) + 1
        ds_containername(ds_info)
        
        cont = ds_info["container_name"]
        x = dq2_ls(cont)
        if x:
            print "Skipping", ds, "- it already exists. Bump the version number"
            continue
        
        dq2_register_container(cont, ds_datasets["datasets_expanded"])
        
        with open(ds_filename, "w") as fd:
            fd.write(dump_all([ds_info, ds_datasets], default_flow_style=False))  

def dq2_register_container(container_name, datasets):
    cmd = "dq2-register-container {0}".format(container_name)
    status, output = getstatusoutput(cmd)
    assert not status, "Failed: {0}".format(output)
    
    p = Popen(["xargs", "dq2-register-datasets-container", container_name], 
              stdin=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate("\n".join(datasets))
    result = p.wait()
    print stdout #, stderr
    assert not result, "Failed: {0}".format(stderr)
    #print "Done:", container_name, result

def dq2_expand_containers(cs):
    """
    Get all datasets inside a list of containers
    """
    # Add end slashes
    cs = [c + "/" if not c.endswith("/") else c for c in cs]
    p = Popen(["xargs", "-P4", "-n1", "dq2-list-datasets-container"], 
              stdin=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate("\n".join(cs))
    result = p.wait()
    assert not result
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
