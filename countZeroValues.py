#!/usr/bin/env python
# =============================================================================
# @file   countZeroValues.py
# @author C. Marin Benito (carla.marin.benito@cern.ch)
# @date   02.07.2015
# =============================================================================
"""Script to number of entries giving zero for a given tree branch"""

# imports
from argparse import ArgumentParser
import ROOT

# main
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("file"  , action="store", type=str, help="file name"           )
    parser.add_argument("branch", action="store", type=str, help="branch to be checked")
    parser.add_argument("-t", "--tree" , default="DecayTree" , action="store", type=str  , help="tree name (def: DecayTree)"             )
    parser.add_argument("-v", "--value", default=0.          , action="store", type=float, help="value to search in the branch (def: 0.)")

    args = parser.parse_args()
    fileName = args.file
    treeName = args.tree
    branch   = args.branch
    value    = args.value

    f = ROOT.TFile(fileName)
    t = f.Get(treeName)
    entries = t.GetEntries()

    n   = t.GetEntries("%s==%s" %(branch, value))
    eff = float(n)/entries*100

    print "Total entries: %25s" %entries
    print "Entries with %s value == %20s: %5s" %(branch, value, n)
    print "Proportion is: %25s %%" %eff
    
# EOF