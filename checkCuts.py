import argparse
import ROOT

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" , default="" , action="store", type=str)
    parser.add_argument("-t", "--tree" , default="" , action="store", type=str)
    parser.add_argument("-c", "--cuts" , default="" , action="store", type=str)
    args = parser.parse_args()
    fileName  = args.file
    treeName  = args.tree
    cuts = args.cuts

    f = ROOT.TFile(fileName)
    t = f.Get(treeName)

    entries = t.GetEntries()
    entries_cuts = t.GetEntries(cuts)
    entries_diff = entries - entries_cuts
    if entries_diff!=0: print "%s entries are not passing the cuts!" %entries_diff
    else: print "All the entries are passing the cuts, well done!"

#EOF