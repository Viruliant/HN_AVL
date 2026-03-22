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

# simple_AVL_test.py

import subprocess, threading, re, os, sys, inspect, shutil, argparse, random, math, fnmatch, json, types

def load_rand(tree, n: int):
    """Insert n random keys into the AVL tree."""
    for _ in range(n):
        key = random.randint(0, 1_000_000)
        tree.insert(key)

def inorder_list(tree):
    """Return an inorder list by repeatedly using index-based search()."""
    result = []
    i = 0
    while True:
        node = tree.search(i)
        if not node:
            break
        result.append(node.key)
        i += 1
    return result

def delete_rand(tree, k: int):
    """Delete k random nodes using inorder indices."""
    for _ in range(k):
        keys = inorder_list(tree)
        if not keys:
            return  # Tree empty

        idx = random.randrange(len(keys))
        key_to_delete = keys[idx]

        print(f"Deleting key at index {idx}: {key_to_delete}")

        # AVL.delete expects an index, not a key
        tree.delete(idx)

        # Optional: verify deletion
        remaining = inorder_list(tree)
        assert key_to_delete not in remaining, "Delete failed: key still present"
        assert remaining == sorted(remaining), "Tree invariant violated"

def main():
    random.seed(42)
    t = AVL()

    load_rand(t, 20)
    print("Initial keys:", inorder_list(t))

    delete_rand(t, 10)
    print("After deletions:", inorder_list(t))

    t.print_tree()

"""

# AVL Tree

"""
INT32_MASK = 0xFFFFFFFF

def int32(x: int) -> int:
    """Force Python int into signed 32‑bit range."""
    x &= INT32_MASK
    return x if x < 0x80000000 else x - 0x100000000

class Node:
    def __init__(self, key: int):
        self.key = int32(key)
        self.left = None
        self.right = None

class AVL:
    def __init__(self):
        self.root = None

    def _height(self, n):
        if not n:
            return 0
        return 1 + max(self._height(n.left), self._height(n.right))

    def _size(self, n):
        if not n:
            return 0
        return 1 + self._size(n.left) + self._size(n.right)

    def search(self, index: int) -> Node:
        node = self.root
        while node:
            left_size = self._size(node.left)
            if index < left_size:
                node = node.left
            elif index == left_size:
                return node
            else:
                index -= left_size + 1
                node = node.right
        return None

    def _rebalance(self, node: Node) -> Node:
        def _rotate_left(x: Node) -> Node:
            y = x.right
            x.right = y.left
            y.left = x
            return y
        def _rotate_right(y: Node) -> Node:
            x = y.left
            y.left = x.right
            x.right = y
            return x
        def _balance(n: Node) -> int:
            return self._height(n.left) - self._height(n.right)
        bf = _balance(node)
        if bf > 1: # Left heavy
            if _balance(node.left) < 0:
                node.left = _rotate_left(node.left)
            return _rotate_right(node)
        if bf < -1: # Right heavy
            if _balance(node.right) > 0:
                node.right = _rotate_right(node.right)
            return _rotate_left(node)
        return node

    def insert(self, key: int) -> Node:
        def _insert(node, key):
            if not node:
                return Node(key)
            if key == node.key:
                return node
            if key < node.key:
                node.left = _insert(node.left, key)
            else:
                node.right = _insert(node.right, key)
            node.height = 1 + max(self._height(node.left), self._height(node.right))
            return self._rebalance(node)
        self.root = _insert(self.root, int32(key))
        return self.root

    def _min_node(self, n):
        while n.left:
            n = n.left
        return n

    def _delete_node(self, node, key):
        if not node:
            return None
        if int32(key) < node.key:
            node.left = self._delete_node(node.left, key)
        elif int32(key) > node.key:
            node.right = self._delete_node(node.right, key)
        else:
            # Node found
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            # Replace with inorder successor
            succ = self._min_node(node.right)
            node.key = succ.key
            node.right = self._delete_node(node.right, succ.key)
        return self._rebalance(node)

    def delete(self, index: int) -> Node:
        target = self.search(index)
        if not target:
            return None
        self.root = self._delete_node(self.root, target.key)
        return self.root

    def print_tree(self, indent: int = 0, prefix: str = "", is_last: bool = True):
        """
        Pretty‑prints the AVL tree using ├── and └── markers.
        Works with the existing AVL Node structure.
        """
        def _print(node, prefix, is_last):
            if not node:
                return
            connector = "└── " if is_last else "├── "
            print(prefix + connector + str(node.key))
            # Children exist?
            has_left = node.left is not None
            has_right = node.right is not None
            # New prefix for children
            new_prefix = prefix + ("    " if is_last else "│   ")
            if has_left: # Left child (never last if right child exists)
                _print(node.left, new_prefix, not has_right)
            # Right child
            if has_right:
                _print(node.right, new_prefix, True)
        _print(self.root, prefix, True)

if __name__ == "__main__":
    main()
