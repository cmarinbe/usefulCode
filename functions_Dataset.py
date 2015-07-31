#!/usr/bin/env python
# ===============================================================
# @file   Dataset_functions.py
# @author Carla Marin (carla.marin.benito@cern.ch)
# @date   24.05.2015
# ===============================================================
"""Useful functions to deal with datasets"""

import os
import ROOT
import numpy as np

def select_nbody(path_base, labels_2body, labels_3body,
                 fileNames_2body, fileNames_3body,
                 treeNames_2body, treeNames_3body, n_body):
    """Select options for 2 or 3body tuples
        Not used anymore"""
    fileNames_2body = [os.path.join(path_base, fN) for fN in fileNames_2body]
    fileNames_3body = [os.path.join(path_base, fN) for fN in fileNames_3body]
    if n_body=="all":
        labels = labels_2body + labels_3body
        fileNames = fileNames_2body + fileNames_3body
        treeNames = treeNames_2body + treeNames_3body
    elif n_body=="2":
        labels = labels_2body
        fileNames = fileNames_2body
        treeNames = treeNames_2body
    elif n_body=="3":
        labels = labels_3body
        fileNames = fileNames_3body
        treeNames = treeNames_3body
    else:
        raise OSError("wrong value of 'n_body' %s. options are: 'all', '2', '3'.")
    return labels, fileNames, treeNames

### Import datasets and related
def get_fullFileNames(base_path, fileNames):
    if isinstance(fileNames, str):
        fullfileNames = os.path.join(base_path, fileNames)
    elif isinstance(fileNames, list):
        fullfileNames = [os.path.join(base_path, fN)
                         for fN in fileNames]
    return fullfileNames

def read_trees(fileNames, treeNames):
    from ROOT import TFile
    files = []
    trees = []
    i = 0
    for fN, tN in zip(fileNames, treeNames):
        files.append(TFile(fN))
        trees.append(files[i].Get(tN))
        i += 1
    print "Files and trees read"
    return files, trees

def importROOTdata(branch_names, fName, treeName="DecayTree"):
    """Import signal and background root files to signal and background numpy arrays for the selected branches
        
        :param branch_names: names of the branches to be imported
        :type branch_names: tuple
        :param fName: name of the root file to be imported.
        :type fName: str
        :param treeName: tree name in the files.
        :type fName: str
        
        :rtype: ndarray
        """
    from root_numpy import root2array, rec2array
    data_array = root2array(fName, treeName, branch_names)
    data_array = rec2array(data_array)
    return data_array

def import_data(fileNames, treeNames, branches_toimport):
    """Extension of importROOTdata to n files"""
    if isinstance(fileNames, str):
        return importROOTdata(branches_toimport, fileNames, treeNames)
    elif isinstance(fileNames, list):
        datasets = [0 for i in range(len(fileNames))]
        data = np.ndarray((0,len(branches_toimport)))
        for i in range(len(fileNames)):
            datasets[i] = importROOTdata(branches_toimport, fileNames[i], treeNames[i])
            data = np.concatenate((data, datasets[i]))
        return data

def import_train_test(sigFiles, sigTrees, bkgFiles, bkgTrees,
                      branches_toimport, train_test_sufix):
    train_sufix, test_sufix = train_test_sufix
    data = []
    for files, trees in zip([sigFiles, bkgFiles], [sigTrees, bkgTrees]):
        if isinstance(files, str):
            files_train = files.replace(".root", "%s.root" %train_sufix)
            files_test  = files.replace(".root", "%s.root" %test_sufix)
        elif isinstance(files, list):
            files_train = [f.replace(".root", "%s.root" %train_sufix) for f in files]
            files_test  = [f.replace(".root", "%s.root" %train_sufix) for f in files]
        data.append( import_data(files_train, trees, branches_toimport) ) # add train
        data.append( import_data(files_test , trees, branches_toimport) ) # add test
    sig_train, sig_test, bkg_train, bkg_test = data
    X_train, y_train = get_x_y(sig_train, bkg_train)
    X_test , y_test  = get_x_y(sig_test , bkg_test )
    return X_train, X_test, y_train, y_test

def get_x_y(sig_data, bkg_data):
    """Get X and y as needed for BDT training in sklearn.
        
        X contains the variables for training while y
        contains the true info of the event: 1 for signal
        and 0 for backgr
        
        :param sig_data: signal dataset
        :type sig_data: ndarray
        :param bkg_data: backgr dataset
        :type bkg_data: ndarray
        
        :return: X, y
        :rtype: tuple"""
    X = np.concatenate((sig_data, bkg_data))
    y = np.concatenate((np.ones(sig_data.shape[0]),
                        np.zeros(bkg_data.shape[0])))
    return X, y

### Copy datasets and related
def copy_file_structure(old_file, tree_name, new_file):
    """Copy the structure of a ROOT file.
        
        :param old_file: file name to copy the structure from
        :type old_file: str
        :param tree_name: name of the tree to analyze
        :type tree_name: str
        :param new_file: name of the file to create
        :type new_file: str
        
        :return: Old TFile, old TTree, new TFile.
        :rtype: tuple
        
        :raises: KeyError: If the tree doesn't exist.
        
        """
    old_file = ROOT.TFile.Open(old_file)
    old_tree = old_file.Get(tree_name)
    if not old_tree:
        raise KeyError("Cannot find tree -> %s" % tree_name)
    new_file = ROOT.TFile.Open(new_file, 'UPDATE') #only change wrt RootUtils
    dirs = tree_name.split('/')
    if len(dirs) > 1:
        for dir_ in dirs[:-1]:
            new_file.mkdir(dir_)
            new_file.cd(dir_)
    return old_file, old_tree, new_file

def copy_tree_with_cuts(old_file, tree_name, new_file_name, cuts, active_branches=["*"], disabled_branches=None):
    """Copy a TTree for a file applying cuts.
        
        The names of the branches to copy, ie, active, can be specified
        to reduce file size.
        
        :param old_file: file name to copy the structure from
        :type old_file: str
        :param tree_name: name of the tree to analyze
        :type tree_name: str
        :param new_file_name: name of the file to create
        :type new_file_name: str
        :param cuts: cuts to apply
        :type cuts: list, string or TCut
        :param active_branches: branches to pass on to the new tree
        :type active_branches: list
        :param disabled_branches: branches to disable after activating
        :type disabled_branches: list
        
        :rtype: boolean
    """
    try:
        old_file, old_tree, new_file = copy_file_structure(old_file, tree_name, new_file_name)
    except Exception, exc:
        print "Cannot reduce %s" % old_file
        print exc
        return False
    # Process cuts
    if isinstance(cuts, (list, tuple)):
        cut_string = ' && '.join(cuts)
    elif isinstance(cuts, str):
        cut_string = cuts
    elif isinstance(cuts, ROOT.TCut):
        cut_string = cuts.GetTitle()
    else:
        return False
    # Which branches to save?
    old_tree.SetBranchStatus("*", 0)
    for branch in active_branches:
        old_tree.SetBranchStatus(branch, 1)
    if disabled_branches:
        for branch in disabled_branches:
            old_tree.SetBranchStatus(branch, 0)
    # Let's do it
    new_tree = old_tree.CopyTree(cut_string)
    if not new_tree:
        print "Error cutting! No events passed the selection!"
        os.remove(new_file_name)
        return False
    new_tree.Write("", ROOT.TObject.kOverwrite)
    new_file.Write("", ROOT.TObject.kOverwrite)
    new_file.Close()
    old_file.Close()
    return True

### Split datasets and related

def add_rdm(fileName, treeName):
    import array
    import numpy as np
    myArrayA = array.array('d', [0.0])
    if not os.path.exists(fileName):
        print "File %s does not exist!" % fileName
        return None
    fileToCopy, tree, fileNew = copy_file_structure(fileName, treeName, fileName.replace('.root', '_new.root'))
    events = tree.GetEntries()
    print "Old tree has %s entries" % events
    treeNew = tree.CloneTree(0)
    branches = {}
    branches["bdt_A"] = treeNew.Branch("bdt_A", myArrayA, "bdt_A/D")
    for i in range(events):
        tree.GetEntry(i)
        myArrayA[0] = np.random.randint(0,2)
        treeNew.Fill()
    treeNew.Write("", ROOT.TObject.kOverwrite)
    fileNew.Close()
    print "########## Finished generating random discriminator"
    return fileName.replace('.root', '_new.root')

### Discretize datasets and related
def discretiseVar(t, nt, varName, bins, verbose=False):
    from array import array
    # def variable and branch that will be added
    var_discretised = array('f',[0.])
    if varName.startswith("log10"): newName = "log10_" + varName[6:-1]
    else: newName = varName
    ANewBranch = nt.Branch('%s_discretised' %newName, var_discretised, '%s_discretised/F' %newName)
    # loop over all entries to fill new
    nentries = t.GetEntries()
    for n in range(nentries):
        t.GetEntry(n)
        if varName.startswith("log10"):
            var_value = ROOT.TMath.log10(getattr(t, varName[6:-1]))
        else:
            var_value = getattr(t, varName)
        var_discretised[0]=-10000 # for entries outside the binning
        for i in range(len(bins)-1):
            if var_value>bins[i] and var_value<bins[i+1]:
                var_discretised[0]=(bins[i+1]+bins[i])/2.
        ANewBranch.Fill()
    if verbose:
        print "#############"
        print "var %s discretized" %varName

def discretiseVar_fromArray(X, bins, verbose=False):
    # def tuples to loop and fill
    X_tuple = X.tolist()
    X_tuple_discretised = [-10000 for x in X_tuple] # for entries outside the binning
    # loop over all entries to fill new
    for i in range(len(X_tuple)):
        for b in range(len(bins)-1):
            if X_tuple[i]>bins[b] and X_tuple[i]<bins[b+1]:
                X_tuple_discretised[i]=(bins[b+1]+bins[b])/2.
    X_discretised = np.array(X_tuple_discretised)
    if verbose:
        print "#############"
        print "var %s discretized" %varName
    return X_discretised

def findMaxValueFiles(fileNames, treeNames, vars):
    if len(treeNames)==1: treeNames = [treeNames[0] for i in range(len(fileNames))]
    max_values = {var: [] for var in vars}
    for fN, tN in zip(fileNames, treeNames):
        f = TFile(fN)
        t = f.Get(tN)
        for var in vars:
            if var.startswith("log10"):
                max_values[var].append(ROOT.TMath.log10(t.GetMaximum(var[6:-1])))
            else:
                max_values[var].append(t.GetMaximum(var))
    for var in vars:
        max_values[var] = max(max_values[var])
    return max_values


#EOF