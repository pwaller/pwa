# -*- coding: utf-8 -*-

import sys

from pprint import pprint

from commando import Application, command, subcommand, version, store, true, param

from minty.main import make_main

def mp_merge(args):
    from hmerge import merge_files
    merge_files(*args)

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
    @param('files', nargs="+")
    def mergeall(self, params):
        from hmerge import merge_files
        from tarfile import open as tarfile_open
        from contextlib import closing
        
        print "Input:", params.files
        
        fileset = set()
        for f in params.files:
            with closing(tarfile_open(f)) as tar:
                fileset |= set(rootfile.path for rootfile in tar.getmembers())
        
        from multiprocessing import Pool
        pool = Pool(4)
        pool.map(mp_merge, [(f, params.files, f) for f in sorted(fileset)])
    
    @subcommand('reduce', help="Reduce many output- files to files by period.")
    @store('-d', '--dummy')
    def reduce(self, params):
        from os import listdir
        files = [f for f in listdir(".") 
                 if f.startswith("output-") and f.endswith(".root")]
        
        def get_period(s): return s.split("-")[1].split("_")[-1]
        
        by_subperiod = {}
        for f in files:
            by_subperiod.setdefault(get_period(f), []).append(f)
            
        from multiprocessing import Pool
        pool = Pool(4)
        
        pool.map(mp_merge, [("period%s.root" % p, files) for p, files in by_subperiod.iteritems()])
        
        by_period = {}
        for p, files in sorted(by_subperiod.iteritems()):
            by_period.setdefault(p[0], []).extend(files)
            
        pool.map(mp_merge, [("period%s.root" % p, files) for p, files in by_period.iteritems()])
        
        from hmerge import merge_files
        merge_files("all.root", ["period%s.root" % p for p in by_period])
        
        print "Done."

    
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
