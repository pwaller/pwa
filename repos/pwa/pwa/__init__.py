# -*- coding: utf-8 -*-

import sys

from os.path import basename
from pprint import pprint

from commando import Application, command, subcommand, version, store, true, param

from minty.main import make_main

import results
import datasets
import jobs
import plot
import fit

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
    mergereduce = results.mergereduce
    dump = results.dump
    dump_grl = results.dump_grl
    dump_files = results.dump_files
    status = results.status
    kick = results.kick
    
    mcupdateinfo = results.mcupdateinfo
    mcrescale = results.mcrescale
    
    make_datasets = datasets.make_datasets
    dsupdate = datasets.dsupdate
    dsbuild = datasets.dsbuild
    
    dscheck = datasets.dscheck
    
    submit = jobs.submit
    
    draw = plot.draw
    
    multifit = fit.multifit

def main():
    from minty.utils import init_root
    from minty.utils.logger import log_level
    from logging import DEBUG
    with log_level(DEBUG):
        init_root()
        Engine().run()
