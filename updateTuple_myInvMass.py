#!/usr/bin/env python
# =============================================================================
# @file   updateTuple_myInvMass.py
# @author C. Marin Benito (carla.marin.benito@cern.ch)
# @date   18.06.2015
# =============================================================================
"""Add invariant mass of 2 electrons to a tuple"""

from ROOT import TFile
from array import array

def addMyInvMass(fileName, treeName):
    file = TFile(fileName,'UPDATE')
    tree = file.Get(treeName)
    # Variables that will be added
    ee_myInvMass = array('f',[0.])
    # Branches to add
    ANewBranch = tree.Branch('ee_myInvMass', ee_myInvMass, 'ee_myInvMass/F')
    # Loop over all entries
    nentries = tree.GetEntries()
    for i in range(nentries):
        tree.GetEntry(i)
        if i%10000 ==0: print 'Entry', i
        # read variables
        eminus_PX = tree.eminus_PX
        eminus_PY = tree.eminus_PY
        eminus_PZ = tree.eminus_PZ
        eminus_PE = tree.eminus_PE
        eplus_PX = tree.eplus_PX
        eplus_PY = tree.eplus_PY
        eplus_PZ = tree.eplus_PZ
        eplus_PE = tree.eplus_PE
        # compute inv m
        E12 = eminus_PE + eplus_PE
        PX12 = eminus_PX + eplus_PX
        PY12 = eminus_PY + eplus_PY
        PZ12 = eminus_PZ + eplus_PZ
        P12_2 = PX12**2 + PY12**2 + PZ12**2
        ee_myInvMass[0] = (E12**2 - P12_2)**(0.5)
        # write inv mass
        ANewBranch.Fill()
    # Close the file
    file.Write()
    file.Close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" , default="" , action="store", type=str, help="file to be updated")
    parser.add_argument("-t", "--tree" , default="" , action="store", type=str, help="tree in file to be updated")
    args = parser.parse_args()
    fileName  = args.file
    treeName  = args.tree
    addMyInvMass(fileName, treeName)

# EOF