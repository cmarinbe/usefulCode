from ROOT import *
from array import array
import ROOT

import getopt
# File to be updated

file = TFile("/u/mrsrv/cmarin/KsTo4l/tuples/Ks4e.root",'UPDATE')
tree = file.Get("Ks4eTuple/DecayTree")

# Variables that will be added

ee_myInvMass = array('f',[0.])
ee0_myInvMass = array('f',[0.])

# Branches to add

ANewBranch = tree.Branch('ee_myInvMass', ee_myInvMass, 'ee_myInvMass/F')
BNewBranch = tree.Branch('ee0_myInvMass', ee0_myInvMass,'ee0_myInvMass/F')

# Write the variables

v_piminus = TLorentzVector()
v_Kplus = TLorentzVector()
nentries = tree.GetEntries()

for i in range(nentries):
    tree.GetEntry(i)
    if i%10000 ==0:
        print 'Entry', i
    piminus_PX = tree.piminus_PX
    piminus_PY = tree.piminus_PY
    piminus_PZ = tree.piminus_PZ
    piminus_PE = tree.piminus_PE
    Kplus_PX = tree.Kplus_PX
    Kplus_PY = tree.Kplus_PY
    Kplus_PZ = tree.Kplus_PZ
    Kplus_PE = tree.Kplus_PE
    v_piminus.SetPxPyPzE(piminus_PX, piminus_PY, piminus_PZ, piminus_PE)
    v_Kplus.SetPxPyPzE(Kplus_PX, Kplus_PY, Kplus_PZ, Kplus_PE)
    piminus_TRACK_Eta[0]=v_piminus.Eta()
    Kplus_TRACK_Eta[0]=v_Kplus.Eta()
    ANewBranch.Fill()
    BNewBranch.Fill()

# Close the file

file.Write()
file.Close()
