
from commands import getstatusoutput
from os.path import basename
from subprocess import Popen

from commando import subcommand, param
from yaml import load

import datasets

def get_tag():
    status, output = getstatusoutput("git describe --tags --exact-match --dirty")
    if status:
        return "dryrun"
    assert not status, "Master repository is not tagged."
    #assert not "dirty" in output, "Master repository is dirty"
    return output.strip()

class Job(object):
    def __init__(self, job_file):
        self.name = basename(job_file).rpartition(".")[0]
        with open(job_file) as fd:
            self.job_info = load(fd)
    
    def submit(self, dry_run=False):
        for ds in self.datasets:
            self.submit_one(ds, dry_run)
    
    def submit_one(self, dataset, dry_run=False):
        ds_info, ds_datasetinfo = datasets.ds_load(dataset)
        ds_name = datasets.ds_name(dataset)
        
        input_name = ds_info["container_name"]
        progname = ".".join([self.name, get_tag()])
        default_outpattern = "user.{user}.{progname}.{dsname}.v{version}/"
        outpattern = self.job_info.get("outpattern", default_outpattern)
        output_name = outpattern.format(progname=progname, user=datasets.user, dsname=ds_name, **ds_info)
    
        command = self.job_info["command"]
        
        tmpdirname = progname + "." + ds_name
        
        p = Popen((["echo"] if dry_run else []) +
                  ["subscripts/generic_submit.sh", 
                   input_name, output_name, 
                   command, tmpdirname,
                   self.job_info.get("submit_extra", "")])
        p.wait()
        
    @property
    def datasets(self):
        if isinstance(self.job_info["dataset"], list):
            return self.job_info["dataset"]
        return [self.job_info["dataset"]]

@subcommand('submit', help='Submit jobs')
@param('jobs', nargs="+")
def submit(self, params):
    tag = get_tag()
    
    if tag != "dryrun":
        p = Popen(["./prepare_submit.sh"])
        assert not p.wait()
    
    for job in params.jobs:
        Job(job).submit(tag == "dryrun")
        
        
