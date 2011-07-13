#! /usr/bin/env python

from logging import getLogger; log = getLogger("pwa.datasets")

from datetime import datetime
from commands import getstatusoutput
from os.path import abspath, basename, isfile
from pkg_resources import resource_listdir, resource_filename
from pprint import pprint
from subprocess import Popen, PIPE

from commando import Application, command, subcommand, version, store, true, param

from yaml import load, load_all, dump_all

from minty.metadata.ami import query_datasets

user = "PeterWaller"

class PwaDataset(object):
    def __init__(self, name, info, datasets):
        args = name, info, datasets["datasets"], datasets["datasets_expanded"]
        self.name, self.info, self.datasets, self.datasets_expanded = args
        info["shortname"] = name
    
    @property
    def container_name(self):
        i = self.info
        return i["container"].format(user=user, dsname=self.name, **i)
    
    @classmethod
    def from_file(cls, filename):
        if not isfile(filename):
            filename = resource_filename("pwa.datasets", filename)
            assert isfile(filename), "Can't find dataset '{0}'".format(filename)
    
        name, _, ext = basename(filename).rpartition(".")
        with open(filename) as fd:
            info, datasets = list(load_all(fd))
        return cls(name, info, datasets)
    
    def to_file(self, filename):
        for dataset in self.datasets:
            dataset.clean()
    
        self.info["update_time"] = datetime.now()
    
        datasets = dict(datasets=self.datasets, 
                        datasets_expanded=self.datasets_expanded)
        data = [self.info, datasets]
        content = dump_all(data, default_flow_style=False)
        with open(filename, "w") as fd:
            fd.write(content)
    
    def check(self):
        cont = dq2_expand_containers([self.container_name])
        known_locally = set(self.datasets_expanded) 
        known_grid = set(cont) if cont else None
        good = known_locally == known_grid
        return good, known_locally, known_grid

    def update_datasets(self):
        # Find datasets matching pattern (which are VALID and EVENTS_AVAILABLE)
        pattern = self.info["pattern"]
        datasets = query_datasets(pattern)
        if not datasets:
            # Fallback to dq2-ls
            log.warning("Couldn't find dataset for pattern {0}".format(pattern))
            log.warning("on AMI. Falling back to dq2-ls.")
            datasets = dq2_ls(pattern)
                
        # Expand containers
        self.datasets = datasets        
        self.datasets_expanded = dq2_expand_containers(d.name for d in datasets)
        
        for dataset in self.datasets:
            if dataset.contents.get("projectname", "").startswith("mc"):
                # Trigger re-loading of mc_info
                if "mc_info" in dataset.contents:
                    del dataset.contents["mc_info"]
                dataset.mc_info
                
    def update_container(self):
    
        good, _, _ = self.check()
        
        if good:
            log.info("Skipping dataset, already consistent with grid {0}"
                     .format(self.name))
            return
        
        self.info["version"] = self.info.get("version", 0) + 1
        
        x = dq2_ls(self.container_name)
        assert not x, "Version number already exists?"
        
        dq2_register_container(self.container_name, self.datasets_expanded)
        log.info("Updated container {0}".format(self.container_name))

@subcommand('make_datasets', help='Build a new dataset')
@param('files', nargs="+")
def make_datasets(self, params):
    #print "Here..", params
    
    for f in params.files:
        items = load_all(f)
        
def list_datasets(pattern="*"):
    from glob import fnmatch
    return [PwaDataset.from_file(x)
            for x in resource_listdir("pwa", "datasets") 
            if x.endswith(".yaml") and fnmatch.fnmatch(x, pattern)]

def get_dataset_mapping(pattern="*"):
    dataset_files = list_datasets(pattern)
    result = {}
    for dsf in dataset_files:
        for ds in dsf.datasets:
            assert not ds.run in result
            result[ds.run] = ds
    return result    

@subcommand('dsupdate', help='Update dataset info')
@param('files', nargs="*")
def dsupdate(self, params):
    fileset = set(abspath(p) for p in params.files)
    
    from IPython.Shell import IPShellEmbed
    ip = IPShellEmbed(["-pdb"])

    for filename in fileset:
        dataset = PwaDataset.from_file(filename)
        
        if "pattern" not in dataset.info:
            print "Skipping dataset (no pattern):", filename
            continue
        
        print "Updating dataset:", filename
        
        dataset.update_datasets()
        
        dataset.to_file(filename)
        
@subcommand('dscheck', help='Check datasets are uptodate')
@param('files', nargs="*")
def dscheck(self, params):
    for filename in params.files:
        dataset = PwaDataset.from_file(filename)
        
        good, known_locally, known_grid = dataset.check()
        log.info("{0:30} : {1} : {2}".format(filename, good, dataset.container_name))
        
            
@subcommand('dsbuild', help='Update dataset info')
@param('files', nargs="*")
def dsbuild(self, params):
    
    for filename in params.files:
        ds = PwaDataset.from_file(filename)
        ds.update_container()
        ds.to_file(filename)
        
        log.info("Updated {0}".format(filename))

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
    if result:
        # Dataset doesn't exist?
        return None
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
