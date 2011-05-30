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
        print get_tag()
        for job in params.jobs:
            pprint(load(open(job)))
        #getstatusoutput(

def get_tag():
    status, output = getstatusoutput("git describe --tags --exact-match --dirty")
    assert not status
    return output.strip()

def main():
    Engine().run()
