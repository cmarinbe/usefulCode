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

    print "%s candidates in the initial tuple"    % entries
    print "%s candidates pass the selection"      % passEntries
    print "The efficiency of the selection is %s" % eff

    textFile = "selection%s.txt" %newName
    with open(textFile, 'w') as output:
        output.write("Selection: \n %s\n" %cuts)
        output.write("File:      \n %s\n" %fileName)
        output.write("Efficiency:\n %s\n" %eff)
    
    return newFileName, eff


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", action="store", type=str, help="file name"       )
    parser.add_argument("cuts", action="store", type=str, help="cuts to apply"   )
    parser.add_argument("-t", "--tree", default="DecayTree" , action="store", type=str, help="tree name (def: DecayTree)"          )
    parser.add_argument("-n", "--name", default="_selection", action="store", type=str, help="sufix for new file (def: _selection)")
    args = parser.parse_args()
    fileName = args.file
    treeName = args.tree
    cuts     = args.cuts
    newFName = args.name
    newFileName, eff = applyCuts(fileName, treeName, cuts, newFName)
    
#EOF
