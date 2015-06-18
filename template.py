#!/usr/bin/env python
# =============================================================================
# @file   fileName.py
# @author C. Marin Benito (carla.marin.benito@cern.ch)
# @date   dd.mm.yy
# =============================================================================
"""Description of the script"""

# imports
import os
import argparse
import ROOT

# definition of functions for this script
def main(arg1):
    print arg1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--arg1", default="", action="store", type=str, help="argument 1")
    args = parser.parse_args()
    arg1  = args.arg1
    main(arg1)


# EOF