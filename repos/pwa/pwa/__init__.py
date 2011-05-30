# -*- coding: utf-8 -*-

import sys

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
        
def main():
    Engine().run()
