import argparse
import ROOT

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default = ""         , action = "store", type = str)
parser.add_argument("-t", "--tree", default = "DecayTree", action = "store", type = str)

args = parser.parse_args()
fileName = args.file
treeName = args.tree

file = ROOT.TFile(fileName)
tree = file.Get(treeName)

entries = tree.GetEntries()

n=0
for i in xrange(entries-1):
    tree.GetEntry(i)
    runNum = tree.runNumber
    eventNum = tree.eventNumber
    tree.GetEntry(i+1)
    if (runNum == tree.runNumber and eventNum == tree.eventNumber):
        n = n+1
    runNum = tree.runNumber
    eventNum = tree.eventNumber


print "Total entries: ", entries
print "Entries with = evt and run numb :", n
    
