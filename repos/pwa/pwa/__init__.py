# -*- coding: utf-8 -*-

import sys

from pprint import pprint

from commando import Application, command, subcommand, version, store, true, param

from minty.main import make_main


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

    @subcommand('mergeall', help='Merge all of the files contained in a tgz')
    @param('-f', '--file')
    def mergeall(self, params):
        from hmerge import merge_files
        from tarfile import open as tarfile_open
        from contextlib import closing
        
        with closing(tarfile_open(params.file)) as tar:
            files = set(f.path for f in tar.getmembers())
        
        for f in files:
            print "Building", f
            merge_files(f, [params.file], pattern=f)
            
    @subcommand('dump', help='Dump basic information')
    @param('files', nargs="+")
    def dump(self, params):
        from ROOT import TFile
        for f in params.files:
            f = TFile.Open(f)
            h = f.cutflow; xa = h.GetXaxis()
            pprint([(h[i], xa.GetBinLabel(i)) for i in xrange(1, xa.GetNbins()+1)])
        
def main():
    Engine().run()
