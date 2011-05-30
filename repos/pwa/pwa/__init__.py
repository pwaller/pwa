# -*- coding: utf-8 -*-

import sys

from commands import getstatusoutput
from pprint import pprint


from commando import Application, command, subcommand, version, store, true, param

from minty.main import make_main

import results
import datasets

class Engine(Application):

    @command(description='Engine - Turbo powered',
            epilog='Use %(prog)s {command} -h to get help on individual commands')
    @version('-v', '--version', version='%(prog)s 0.1')
    @store('-k', '--key', default='.', help="Key to start the engine")
    def main(self, params):
        """
        Will not be executed. A sub command is required. This function exists to provide
        common parameters for the subcommands and some generic stuff like version and
        metadata
        """
        pass

    mergeall = results.mergeall
    reduce = results.reduce
    dump = results.dump
    
    make_datasets = datasets.make_datasets
    dsupdate = datasets.dsupdate
    dsbuild = datasets.dsbuild
    
    @subcommand('submit', help='Build a new dataset')
    @param('jobs', nargs="+")
    def submit(self, params):
        from yaml import load
        from subprocess import Popen
        print get_tag()
        
        p = Popen(["prepare_submit.sh"])
        p.wait()
        
        for job in params.jobs:
            print job
            job_info = load(open(job))
            print job_info
            ds_info, ds_datasetinfo = datasets.ds_load(job_info["dataset"])
            ds_name = datasets.ds_name(job_info["dataset"])
            
            input_name = ds_info["container_name"]
            progname = ".".join([job_info["progname"], get_tag()])
            output_name = ds_info["outpattern"].format(progname=progname, user=datasets.user, dsname=ds_name, **ds_info)
            
            command = job_info["command"]
            
            
            p = Popen(["echo", "subscripts/generic_submit.sh", 
                       input_name, output_name, 
                       command, "tmpdirname", 
                       job_info.get("submit_extra", "")])
            p.wait()            

def get_tag():
    status, output = getstatusoutput("git describe --tags --exact-match --dirty")
    assert not status, "Master repository is not tagged."
    #assert not "dirty" in output, "Master repository is dirty"
    return output.strip()

def main():
    Engine().run()
