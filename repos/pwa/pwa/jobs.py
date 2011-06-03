
import re

from commands import getstatusoutput
from os.path import basename, exists, join as pjoin
from os import makedirs
from subprocess import Popen, PIPE

from commando import subcommand, param
from yaml import load, dump

import datasets

RE_JOBSETID = re.compile("^\s*JobsetID\s*:\s*(\d+)\s*", re.M)

def get_tag():
    status, output = getstatusoutput("git describe --tags --exact-match --dirty")
    if status:
        return "dryrun"
    assert not status, "Master repository is not tagged."
    #assert not "dirty" in output, "Master repository is dirty"
    return output.strip()

class Job(object):
    def __init__(self, tag, job_file):
        self.tag = tag
        self.name = basename(job_file).rpartition(".")[0]
        with open(job_file) as fd:
            self.job_info = load(fd)
    
    def save_for_reaper(self, output, error, output_name):
        if not exists("need_reap"):
            makedirs("need_reap")
        jsid = RE_JOBSETID.search(output)
        assert jsid
        (jsid,) = jsid.groups()
        jobset_filename = pjoin("need_reap", jsid + ".yaml")
        
        from lockfile import LockFile
        with LockFile(jobset_filename):
            jobset_info = load(open(jobset_filename)) if exists(jobset_filename) else {}
            
            jobset_info["tag"] = self.tag
            jobset_info["name"] = self.name
            jobset_info["output"] = output
            jobset_info["error"] = output
            jobset_info.setdefault("datasets", set()).add(output_name)
            
            with open(jobset_filename, "w+") as fd:
                dump(jobset_info, fd)        
    
    def submit(self, dry_run=False):
        for ds in self.datasets:
            self.submit_one(ds, dry_run)
    
    def submit_one(self, dataset, dry_run=False):
        ds_info, ds_datasetinfo = datasets.ds_load(dataset)
        ds_name = datasets.ds_name(dataset)
        
        input_name = ds_info["container_name"]
        progname = ".".join([self.name, self.tag])
        default_outpattern = "user.{user}.{progname}.{dsname}.v{version}/"
        outpattern = self.job_info.get("outpattern", default_outpattern)
        output_name = outpattern.format(progname=progname, user=datasets.user, dsname=ds_name, **ds_info)
    
        command = self.job_info["command"]
        
        tmpdirname = progname + "." + ds_name
        
        if "prun" in self.job_info:
            prun = self.job_info["prun"].format(
                command=command.replace("\n", ""),
                input_dataset=input_name,
                output_dataset=output_name,
                tag=self.tag,
                name=self.name).replace("\n", " \\\n")
            print prun
            
            p = Popen("prun " + prun, shell=True, stdout=PIPE, stderr=PIPE)
            
            stdout, stderr = p.communicate()
            result = p.wait()
            if result:
                print self.name, stdout, stderr
                raise RuntimeError("Yuck..")
            print stdout, stderr
        else:
        
            p = Popen((["echo", "JobsetID : 1"] if dry_run else []) +
                      ["subscripts/generic_submit.sh", 
                       input_name, output_name, 
                       command, tmpdirname,
                       self.job_info.get("submit_extra", "")],
                      stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            result = p.wait()
            if result:
                print self.name, stdout, stderr
                raise RuntimeError("Yuck..")
            print stdout, stderr
        self.save_for_reaper(stdout, stderr, output_name)
        
    @property
    def datasets(self):
        if isinstance(self.job_info["dataset"], list):
            return self.job_info["dataset"]
        return [self.job_info["dataset"]]

def submit_job(args):
    job, tag, dryrun = args
    Job(tag, job).submit(dryrun)

@subcommand('submit', help='Submit jobs')
@param('jobs', nargs="+")
def submit(self, params):
    tag = get_tag()
    
    if tag != "dryrun":
        p = Popen(["./prepare_submit.sh"])
        assert not p.wait()
    
    from multiprocessing import Pool
    p = Pool(4)
    
    p.map(submit_job, [(job, tag, tag == "dryrun") for job in params.jobs])

@subcommand('reaper', help='Wait for job to complete, download results')
@param('jobs', nargs="+")
def reaper(self, params):
    from os import listdir
    
