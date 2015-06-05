import ROOT
from ROOT import TFile, TTree

fileName = "/u/mrsrv/cmarin/KsTo4l/tuples/24032014_MCKs2pipiee_looseSel_DOCA/Ks2pipiee.root"
treeName = "Ks2e2piTuple/DecayTree"

file = TFile(fileName)
tree = file.Get(treeName)
entries = tree.GetEntries()

trackSelection = "piplus_IPCHI2_OWNPV > 50 && piplus_TRACK_GhostProb < 0.3 && piminus_IPCHI2_OWNPV > 50 && piminus_TRACK_GhostProb < 0.3 && eplus_IPCHI2_OWNPV > 50 && eplus_TRACK_GhostProb < 0.3 && eminus_IPCHI2_OWNPV > 50 && eminus_TRACK_GhostProb < 0.3"

pidSelection = "piplus_PIDK < 5 && piminus_PIDK < 5 && eplus_PIDe > -4 && eminus_PIDe > -4"

KsSelection = "KS0_MAXDOCA < 0.3 && KS0_TAU > 0.0008953 && KS0_IP_OWNPV < 1 && KS0_MM < 800"

selection = trackSelection+"&&"+pidSelection+"&&"+KsSelection

cutTree = tree.CopyTree(selection)
passEntries = float(cutTree.GetEntries())
genEvents = 500000
eff = passEntries/genEvents

print "%s events were generated" % genEvents
print "%s candidates pass the selection" % passEntries
print "The efficiency of the selection over generated events is %s" % eff