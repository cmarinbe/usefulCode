#!/usr/bin/env python
#============================================================================
# @file   countMultipleCandidates.py
# @author Carla Marin (cmarin@ecm.ub.edu)
# @date   01.07.2015
#=============================================================================
"""Script to save the content off all .root files in a folder as .png"""
from argparse import ArgumentParser
import ROOT
from ROOT import TFile

def countMultCandidates(tree, fileName="multCand.txt"):
    """Returns the number and % of multiple candidates.
        Assumes all entries with same runNum and evtNum are consecutive.
        :param tree: tree whose candidates want to be checked
        :type  tree: TTree
    """
    results = {}
    entries = tree.GetEntries()
    i = 0
    # loop over all events in the tree
    while i < range(entries):
        tree.GetEntry(i)
        n = 1
        runNum   = t.runNumber
        eventNum = t.eventNumber
        for j in range(entries-i-1):
            tree.GetEntry(i+j+1)
            if (runNum == tree.runNumber and evtNum == tree.eventNumber): n = n+1
            else: break
        if n not in results.keys(): results[n] = 1
        else: results[n] += 1
        i = i+n
    # write results
    n_cand_list = results.keys()
    n_cand_list.sort()
    with open(fileName, 'w') as output:
        for n_cand_perEvent in n_cand_list:
            n_evts = results[n_cand_perEvent]
            n_cand_sameMult = n_cand_perEvent*n_evts
            output.write( "Events with %s candidates: %10s (%s candidates)\n"
                         %(n_cand_perEvent, n_evts, n_cand_sameMult) )
    return results



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("file" , action = "store", type = str, help="root file")
    parser.add_argument("-t", "--tree"   , default = "DecayTree"   , action = "store", type = str, help="tree name in the root file")
    parser.add_argument("-o", "--outFile", default = "multCand.txt", action = "store", type = str, help="name for the results file")
    args   = parser.parse_args()
    fileName = args.file
    treeName = args.tree
    outName  = args.outFile
    # read file and tree
    f = ROOT.TFile(fileName)
    t = f.Get(treeName)
    results = countMultCandidates(tree, outName)

n=0
