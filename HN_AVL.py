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

# HN_AVL.py

import subprocess, threading, re, os, sys, inspect, shutil, argparse, random, math, fnmatch, json, types

"""
## Operational Logic & Complexities

Because this is a **Nested** structure, your operations scale based on the depth of the path () and the number of nodes at each level ().

| Operation | Time Complexity | Description |
|  |  |  |
| **Path Insertion** |  | We perform a logarithmic insert for every step in the path. |
| **Positional Access** |  | Accessing "Index 2 of Index 0" (e.g., `ex_tree[0][2]`). |
| **Space Complexity** |  | Total nodes across all levels, where  is the total count of strings. |

### Implementation Insight: The "Missing" Child Tree

When you first insert "bar", `child_tree` should probably remain `None` to save memory. Only when the path-parser sees a slash (e.g., `"bar/foo"`) should the code instantiate a new `NestedAVL()` inside the "bar" node. This keeps your memory footprint lean if most nodes don't have children.

"""

def main():

    # ex_tree
    # ├── bar
    # │   ├── foo
    # │   └── foo
    # └── par

    ex_tree = NestedAVL()
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

class Node:
    # The building block of the tree.
    # Each node is a "container" that can hold its own nested tree.
    def __init__(self, key: str):
        self.key = key # The string identifier (e.g., "bar").
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1 # Augmented total of nodes in the *current* level's subtree (for  indexing).
        self.child_tree = None  # Initialized only when a child is added
# **`child_tree`**:  A pointer to a *new* instance of `NestedAVL`, representing the nested strings (e.g., the "foos" inside "bar").

### Core AVL & Order Statistic Logic

# These functions handle the balancing and indexing of a single level of the hierarchy.

class NestedAVL:
    def __init__(self):
        self.root = None

    def _get_height(self, node: Node) -> int:
        """Returns the height of a node, handling None as 0."""
        return node.height if node else 0

    def _get_size(self, node: Node) -> int:
        """Returns the augmented subtree size, handling None as 0."""
        return node.size if node else 0

    def _update_metadata(self, node: Node):
        """
        Recalculates node.height and node.size based on children.
        Formula: size = 1 + left.size + right.size
        """
        if node:
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
            node.size = 1 + self._get_size(node.left) + self._get_size(node.right)

    def _rotate_left(self, x: Node) -> Node:
        """Performs a left rotation and updates metadata for affected nodes."""
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_metadata(x)
        self._update_metadata(y)
        return y

    def _rotate_right(self, y: Node) -> Node:
        """Performs a right rotation and updates metadata for affected nodes."""
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_metadata(y)
        self._update_metadata(x)
        return x

    def _rebalance(self, node: Node) -> Node:
        """Checks balance factors and performs necessary rotations."""
        if not node:
            return None
        
        self._update_metadata(node)
        balance = self._get_height(node.left) - self._get_height(node.right)

        # Left Heavy
        if balance > 1:
            if self._get_height(node.left.left) < self._get_height(node.left.right):
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
            
        # Right Heavy
        if balance < -1:
            if self._get_height(node.right.right) < self._get_height(node.right.left):
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    ### Search and Retrieval

    # How we find specific nodes or indices within one level.

    def insert_at_level(self, key: str) -> Node:
        """
        Standard OST-AVL insertion. 
        If key exists, treats it as a duplicate (Separate Node approach).
        Returns the reference to the newly created/inserted Node.
        Complexity: $O(\\log n)$
        """
        new_node_ref = [None] # Use list to capture reference from recursive calls

        def _insert(node, key):
            if not node:
                new_node = Node(key)
                new_node_ref[0] = new_node
                return new_node
            
            if key < node.key:
                node.left = _insert(node.left, key)
            else:
                # Key >= node.key handles duplicates by inserting into right subtree
                node.right = _insert(node.right, key)
                
            return self._rebalance(node)

        self.root = _insert(self.root, key)
        return new_node_ref[0]

    def find_first(self, key: str) -> Node:
        """
        Locates the first occurrence of a key at the current level.
        Used by the path-parser to navigate downwards.
        """
        curr = self.root
        first_found = None
        while curr:
            if curr.key == key:
                first_found = curr
                # Search left to find the "first" in a duplicate-heavy tree
                curr = curr.left
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return first_found

    def select(self, index: int) -> Node:
        """
        Returns the Node at a specific 0-based index using subtree sizes.
        Complexity: $O(\\log n)$
        """
        curr = self.root
        while curr:
            left_size = self._get_size(curr.left)
            if index == left_size:
                return curr
            elif index < left_size:
                curr = curr.left
            else:
                index -= (left_size + 1)
                curr = curr.right
        return None

    ## Hierarchical Path Logic

    # Coordinates multiple `NestedAVL` instances.

    def get_rank(self, key: str) -> int:
        """
        Returns the 0-based index (rank) of the first occurrence of key.
        Because duplicates (key >= node.key) are always in the right subtree, 
        the first occurrence is the first time we encounter the key during search.
        """
        curr = self.root
        rank = 0
        while curr:
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                rank += self._get_size(curr.left) + 1
                curr = curr.right
            else:
                # Found the key. All nodes in left subtree are < key.
                return rank + self._get_size(curr.left)
        return -1

    def insert_path(self, path: str):
        # 1. Split path and prepare to iterate
        segments = path.strip("/").split("/")
        current_tree = self
        
        i = 0
        while i < len(segments):
            segment = segments[i]
            target_index = 0  # Default to the first occurrence
            
            # Check if next segment is an index like [1]
            if i + 1 < len(segments) and segments[i+1].startswith("["):
                try:
                    # Parse the number inside [n]
                    target_index = int(segments[i+1][1:-1])
                    i += 1 # Consume the index segment
                except ValueError:
                    pass

            # Locate the first instance of this key
            first_rank = current_tree.get_rank(segment)
            
            # Find existing at position OR create new
            target_node = None
            if first_rank != -1:
                potential = current_tree.select(first_rank + target_index)
                if potential and potential.key == segment:
                    # Only reuse if NOT the last segment or if index was explicitly specified
                    if i + 1 < len(segments) or (i + 1 < len(segments) and segments[i+1].startswith("[")):
                        target_node = potential

            if not target_node:
                target_node = current_tree.insert_at_level(segment)

            # If not found at that specific position, insert it
            if not target_node:
                target_node = current_tree.insert_at_level(segment)

            # Descend
            if not target_node.child_tree:
                target_node.child_tree = NestedAVL()
            current_tree = target_node.child_tree
            i += 1

    def print_tree(self, indent: int = 0):
        """
        Recursively prints the hierarchy.
        Performs in-order traversal of the AVL tree at the current level,
        then descends into nested child trees.
        """
        def _print_node(node, current_indent):
            if not node:
                return
            
            # 1. Traverse Left Subtree
            _print_node(node.left, current_indent)
            
            # 2. Print Current Node Metadata
            prefix = "  " * current_indent
            print(f"{prefix}├── {node.key} (size={node.size}, height={node.height})")
            
            # 3. Traverse Nested Child Tree (if it exists and has nodes)
            if node.child_tree and node.child_tree.root:
                node.child_tree.print_tree(current_indent + 1)
            
            # 4. Traverse Right Subtree
            _print_node(node.right, current_indent)

        _print_node(self.root, indent)
        
if __name__ == "__main__":
    main()
