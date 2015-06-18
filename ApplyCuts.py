#!/usr/bin/env python
# =============================================================================
# @file   ApplyCuts.py
# @author C. Marin Benito (carla.marin.benito@cern.ch)
# @date   18.06.2015
# =============================================================================
"""Script to copy a tuple with cuts"""

# imports
import argparse
import ROOT
from ROOT import TFile, TTree

# definition of functions for this script
def applyCuts(fileName, treeName, cuts, newName="_seletion"):
    file = TFile(fileName)
    tree = file.Get(treeName)
    entries = tree.GetEntries()
    
    newFileName = fileName.replace(".root", "%s.root" %newName)
    newFile = TFile(newFileName, "recreate")
    
    cutTree = tree.CopyTree(cuts)
    passEntries = float(cutTree.GetEntries())
    cutTree.Write()
    newFile.Close()
    
    eff = passEntries/entries

    print "%s candidates in the initial tuple" % entries
    print "%s candidates pass the selection" % passEntries
    print "The efficiency of the selection is %s" % eff

    return newFileName


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default=""          , action="store", type=str, help="file name"       )
    parser.add_argument("-t", "--tree", default=""          , action="store", type=str, help="tree name"       )
    parser.add_argument("-c", "--cuts", default=""          , action="store", type=str, help="cuts to apply"   )
    parser.add_argument("-n", "--name", default="_seletion" , action="store",           help="name of new file")
    args = parser.parse_args()
    fileName = args.file
    treeName = args.tree
    cuts     = args.cuts
    newFName = args.name
    newFileName = applyCuts(fileName, treeName, cuts, newFName)

#EOF