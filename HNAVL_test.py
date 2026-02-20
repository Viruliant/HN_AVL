#!/usr/bin/env python3
# coding=utf-8
# Copyright (C) 2026 Roy Pfund. All rights reserved.
#
# Permission is  hereby  granted,  free  of  charge,  to  any  person
# obtaining a copy of  this  software  and  associated  documentation
# files  (the  "Software"),  to  deal   in   the   Software   without
# restriction, including without limitation the rights to use,  copy,
# modify, merge, publish, distribute, sublicense, and/or sell  copies
# of the Software, and to permit persons  to  whom  the  Software  is
# furnished to do so.
#
# The above copyright notice and  this  permission  notice  shall  be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT  WARRANTY  OF  ANY  KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES  OF
# MERCHANTABILITY,   FITNESS   FOR   A   PARTICULAR    PURPOSE    AND
# NONINFRINGEMENT.  IN  NO  EVENT  SHALL  THE  AUTHORS  OR  COPYRIGHT
# OWNER(S) BE LIABLE FOR  ANY  CLAIM,  DAMAGES  OR  OTHER  LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING  FROM,
# OUT OF OR IN CONNECTION WITH THE  SOFTWARE  OR  THE  USE  OR  OTHER
# DEALINGS IN THE SOFTWARE.
######################################################################

# HNAVL_test.py

import subprocess, threading, re, os, sys, inspect, shutil, argparse, random, math, fnmatch, json, types

import HNAVLib

def main():

# Hierarchical AVL Tree Structure:
# ├── bar
# │   ├── bar/foo
# │   ├── bar/foo
# ├── par
# 
# let's test adding to duplicates:
# ├── bar
# │   ├── bar/foo
# │   │   ├── bar/foo/apple
# │   ├── bar/foo
# │   │   ├── bar/foo/orange
# ├── par


    ex_tree = HNAVLib.tree.HNAVL()
    ex_tree.insert_path("bar")
    ex_tree.insert_path("bar/foo")
    ex_tree.insert_path("bar/foo")
    ex_tree.insert_path("par")

    print("Hierarchical AVL Tree Structure:")
    ex_tree.print_tree()

    print("\nlet's test adding to duplicates:")
    ex_tree.insert_path("bar/foo/[0]/apple")
    ex_tree.insert_path("bar/foo/[1]/orange")
    ex_tree.print_tree()

    print("\nlet's see some documentation:")

    HNAdoc = HNAVLib.tree.HNAVL()
    HNAVLib.HNAVLdoc.populateintoHNAVL(HNAdoc)
    # HNAVLib.HNAVLdoc.populateintoHNAVL(HNAdoc) #operator error
    HNAdoc.print_tree()

if __name__ == "__main__":
    main()
