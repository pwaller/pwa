from optparse import OptionParser

import minty

import ROOT as R


def main():
    
    parser = OptionParser()
    options, input_filenames = parser.parse_args()
    
    for filename in input_filenames:
        f = R.TFile(filename)
        print filename
        print " Exceptions:", f.exception_count.GetVal()
        print " Keys:", len(f.GetListOfKeys())
