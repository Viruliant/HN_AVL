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

# RB_test.py

'''
implementing 2-3-4 trees using RBtrees, all nodes as 2-nodes. A
2-node requires one red/black node, a 3-node requires two red/black
nodes, and a 4-node requires 3 red/black nodes. This will inherently
make the tree deeper, but the benefits outweigh this slight overhead.

                        [var]=black (var)=red

         +-+-+-+  |          +-+-+-+-+-+            |  +-+-+-+-+-+-+-+
         | |A| |  |          | |A| |B| |            |  | |A| |B| |C| |
         +++-+++  |          +++-+++-+++            |  +++-+++-+++-+++
          |   |   |           |   |   |             |   |   |   |   |
          v   v   |           v   v   v             |   v   v   v   v
          1   2   |           1   2   3             |   1   2   3   4
                  |                                 |
                  |       [B]            [A]        |        [B]
                  |      /   \\          /   \\       |       /   \\
           [A]    |   (A)     (3)    (1)     (B)    |    (A)     (C)
           / \\    |   / \\                    / \\    |    / \\     / \\
          1   2   |  1   2        OR        2   3   |   1   2   3   4

Here are the bottom 7 cases above translated into YAML format.

--------


```yaml
!2node:
  first: 1
  {!node: { content: A }}
  second: 2
```

the 1node above can be represented as:

```yaml
root:
  node: { color: black, content: A }
  left: 1
  right: 2

```

--------

```yaml
!3node:
  - first: 1
  - {!node: { content: A }}
  - second: 2
  - {!node: { content: B }}
  - third: 3
```

the 3node above can be represented as:

```yaml
root:
  node: { color: black, content: B }
  left:
    node: { color: red, content: A }
    left: 1
    right: 2
  right: 3

```

or

```yaml
root:
  node: { color: black, content: B }
  left: 1
  right:
    node: { color: red, content: C }
    left: 2
    right: 3
```

--------

```yaml
!4node:
    - first: 1
    - {!node: { content: A }}
    - second: 2
    - {!node: { content: B }}
    - third: 3
    - {!node: { content: C }}
    - fourth: 4
```

the 4node above can be represented as:

```yaml
root:
  node: { color: black, content: B }
  left:
    node: { color: red, content: A }
    left: 1
    right: 2
  right:
    node: { color: red, content: C }
    left: 3
    right: 4
```

'''

import subprocess, threading, re, os, sys, inspect, shutil, argparse, random, math, fnmatch, json, types

def load_rand(tree, n: int):
    for _ in range(n):
        key = random.randint(0, 1000000)
        tree.insert(key)

def inorder_list(tree):
    return list(tree.inorder_iterator())

def delete_rand(tree, k):
    """Delete k random keys from the tree using inorder indices."""
    for _ in range(k):
        keys = inorder_list(tree)
        if not keys:
            return  # tree empty

        idx = random.randrange(len(keys))
        key_to_delete = keys[idx]

        print(f"Deleting key at index {idx}: {key_to_delete}")
        tree.delete(key_to_delete)

        # Optional: verify the key is gone
        remaining = inorder_list(tree)
        assert key_to_delete not in remaining, "Delete failed: key still present"

        # Optional: verify sorted order
        assert remaining == sorted(remaining), "Tree invariant violated"

def main():
    '''
    $ ./RB_test.py 
    Initial keys: [26225, 31244, 33326, 91161, 98246, 107473, 116739, 146316, 234053, 256787, 288389, 442417, 571858, 619176, 670487, 709570, 772246, 776646, 777572, 935518]
    Deleting key at index 6: 116739
    Deleting key at index 7: 234053
    Deleting key at index 16: 777572
    Deleting key at index 0: 26225
    Deleting key at index 6: 256787
    Deleting key at index 11: 709570
    Deleting key at index 10: 670487
    Deleting key at index 11: 776646
    Deleting key at index 8: 571858
    Deleting key at index 6: 288389
    After deletions: [31244, 33326, 91161, 98246, 107473, 146316, 442417, 619176, 772246, 935518]
    '''
    random.seed(42) # Same random nums
    t = RedBlackTree()
    load_rand(t, 20)
    print("Initial keys:", inorder_list(t))
    delete_rand(t, 10)
    print("After deletions:", inorder_list(t))

class RedBlackTree:
    def __init__(self):
        self.root = None
    RED = False
    BLACK = True
    class RBNode:
        def __init__(self, key: int, color: bool = False):
            self.key = key
            self.left = None
            self.right = None
            self.color = color # False: red, True: black
    def _is_red(self, node):
        return node is not None and node.color == self.RED
    def color_flip(self, node: RBNode):
        node.color = not node.color
        if node.left: node.left.color = not node.left.color
        if node.right: node.right.color = not node.right.color

    def is_2node(self, node): # **Black node with no red children -> 2‑node**
        return node and node.color == self.BLACK and \
               not self._is_red(node.left) and not self._is_red(node.right)
    def is_3node(self, node): # **Black node with one red child -> 3‑node**
        return node and node.color == self.BLACK and \
               (self._is_red(node.left) ^ self._is_red(node.right))
    def is_4node(self, node): # **Black node with two red children -> 4‑node**
        return node and node.color == self.BLACK and \
               self._is_red(node.left) and self._is_red(node.right)

    def split_n4splitn2(self, b_node: RBNode):
#                                                               +-+-+-+
#                                                               | |B| |
#                          [var]=black (var)=red                +++-+++
# +-+-+-+-+-+-+-+                                               /     \
# | |A| |B| |C| |        [B]                    (B)         +-+-+-+ +-+-+-+
# +++-+++-+++-+++       /   \                  /   \        | |A| | | |C| |
#  |   |   |   |     (A)     (C)    -->     [A]     [C]     +++-+++ +++-+++
#  v   v   v   v     / \     / \            / \     / \      |   |   |   |
#  1   2   3   4    1   2   3   4          1   2   3   4     v   v   v   v
#                                                            1   2   3   4
        # Standard color flip: 4-node becomes two 2-nodes, 
        # and the middle (b_node) pushes RED up.
        b_node.color = self.RED
        if b_node.left: b_node.left.color = self.BLACK
        if b_node.right: b_node.right.color = self.BLACK
        return b_node
    # 4‑node is left child of a 2‑node
    def split_n4leftofn2(self, a_node: RBNode):
#            +-+-+-+                                          +-+-+-+-+-+
#            | |D| |        [var]=black (var)=red             | |B| |D| |
#            +++-+++                                          +++-+++-+++
#            /    |         [D]                [D]           /     |   \
#           /     v        /   \              /   \         /      |    V
# +-+-+-+-+-+-+-+ 5      [B]    5           (B)    5  +-+-+-+   +-+-+-+ 5
# | |A| |B| |C| |       /   \      -->     /   \      | |A| |   | |C| |
# +++-+++-+++-+++    (A)     (C)        [A]     [C]   +++-+++   +++-+++
#  |   |   |   |     / \     / \        / \     / \    |   |     |   |
#  v   v   v   v    1   2   3   4      1   2   3   4   v   v     v   v
#  1   2   3   4                                       1   2     3   4
        c_node = a_node.left
        # C becomes red, A and C's children become black
        c_node.color = self.RED
        if c_node.left: c_node.left.color = self.BLACK
        if c_node.right: c_node.right.color = self.BLACK
        return a_node
    # 4‑node is right child of a 2‑node
    def split_n4rightofn2(self, d_node: RBNode):
# +-+-+-+                                              +-+-+-+-+-+
# | |A| |               [var]=black (var)=red          | |A| |C| |
# +++-+++                                              +++-+++-+++
#  |    \               [A]               [A]           /   |    \
#  v     \             /   \             /   \         V    |     \
#  1 +-+-+-+-+-+-+-+  1    [C]          1    (C)       1 +-+-+-+ +-+-+-+
#    | |B| |C| |D| |      /   \    -->      /   \        | |B| | | |D| |
#    +++-+++-+++-+++   (B)     (D)       [B]     [D]     +++-+++ +++-+++
#     |   |   |   |    / \     / \       / \     / \      |   |   |   |
#     v   v   v   v   2   3   4   5     2   3   4   5     v   v   v   v
#     2   3   4   5                                       2   3   4   5
        b_node = d_node.right
        # B becomes red, its children become black
        b_node.color = self.RED
        if b_node.left: b_node.left.color = self.BLACK
        if b_node.right: b_node.right.color = self.BLACK
        return d_node
    # 4‑node is left child of a 3‑node
    def split_n4leftofn3(self, d_node: RBNode):
#          +-+-+-+-+-+                                             +-+-+-+-+-+-+-+
#          | |D| |E| |                                             | |B| |D| |E| |
#          +++-+++-+++          [var]=black (var)=red              +++-+++-+++-+++
#           /   |   |                                               /   |   |   |
#          /    v   v        [D]                    [D]            /    |   v   v
#         /     5   6       /   \                  /   \          /     |   5   6
# +-+-+-+-+-+-+-+          /     (E)              /     (E)   +-+-+-+ +-+-+-+
# | |A| |B| |C| |       [B]      / \    -->    (B)      / \   | |A| | | |C| |
# +++-+++-+++-+++      /   \    5   6         /   \    5   6  +++-+++ +++-+++
#  |   |   |   |    (A)     (C)            [A]     [C]         |   |   |   |
#  v   v   v   v    / \     / \            / \     / \         v   v   v   v
#  1   2   3   4   1   2   3   4          1   2   3   4        1   2   3   4
        b_node = d_node.left
        # B becomes red, its children become black
        b_node.color = self.RED
        if b_node.left: b_node.left.color = self.BLACK
        if b_node.right: b_node.right.color = self.BLACK
        return d_node
    # 4‑node is the middle child of a 3‑node
    def split_n4midofn3(self, e_node: RBNode):
# +-+-+-+-+-+                                              +-+-+-+-+-+-+-+
# | |A| |B| |                 [var]=black (var)=red        | |A| |B| |D| |
# +++-+++-+++                                              +++-+++-+++-+++
#  |   |   \                 [E]                 [C]        |   |   |    \
#  v   v    \                / \                /   \       v   v   |     \
#  1   2     \            (A)   6              /     \      1   2   |      \
#      +-+-+-+-+-+-+-+   /   \       -->    (A)       (E)       +-+-+-+ +-+-+-+
#      | |C| |D| |E| |  1     [C]          /   \     /   \      | |C| | | |E| |
#      +++-+++-+++-+++       /   \        1  [B]     [D]  6     +++-+++ +++-+++
#       |   |   |   |     (B)     (D)        / \     / \         |   |   |   |
#       v   v   v   v     / \     / \       2   3   4   5        v   v   v   v
#       3   4   5   6    2   3   4   5                           3   4   5   6
        c_node = e_node.left.right
        # C becomes red, its children become black
        c_node.color = self.RED
        if c_node.left: c_node.left.color = self.BLACK
        if c_node.right: c_node.right.color = self.BLACK
        return e_node
    # 4‑node is right child of a 3‑node
    def split_n4rightofn3(self, b_node: RBNode):
#   +-+-+-+-+-+                                               +-+-+-+-+-+-+-+
#   | |A| |E| |                                               | |A| |C| |E| |
#   +++-+++-+++            [var]=black (var)=red              +++-+++-+++-+++
#    |   |   |                                                 |  |     |  |
#    v   |   v          [B]                    [B]             v  |     |  v
#    1   |   6         /   \                  /   \            1  |     |  6
# +-+-+-+-+-+-+-+   (A)     \       -->    (A)     \          +-+-+-+ +-+-+-+
# | |B| |C| |D| |   / \      [D]           / \      (D)       | |B| | | |D| |
# +++-+++-+++-+++  1   2    /   \         1   2    /   \      +++-+++ +++-+++
#  |   |   |   |         (C)     (E)            [C]     [E]    |   |   |   |
#  v   v   v   v         / \     / \            / \     / \    v   v   v   v
#  2   3   4   5        3   4   5   6          3   4   5   6   2   3   4   5
        d_node = b_node.right
        # D becomes red, its children become black
        d_node.color = self.RED
        if d_node.left: d_node.left.color = self.BLACK
        if d_node.right: d_node.right.color = self.BLACK
        return b_node

# every black node means either a 2node 3node or 4node

    def insert_into_leaf(self, parent, key):
        """Insert key under a 2‑ or 3‑node parent. No rotations."""
        new_node = self.RBNode(key, self.RED)
        # Insert left or right based on key
        if key < parent.key: parent.left = new_node # parent.left must be None here
        else: parent.right = new_node # parent.right must be None here

    def insert(self, key: int):
        if self.root is None: # tree was empty
            self.root = self.RBNode(key, self.BLACK)
            return
        if self.is_4node(self.root): # Split 4-node before descending
            self.split_n4splitn2(self.root)
            self.root.color = self.BLACK
        self._insert_recursive(self.root, key) # Start recursion

    def _insert_recursive(self, node, key):
        if key == node.key: return 
        # --- RED CHECKS: Determine 3-way direction ---
        # If a child is red, we are conceptually inside a 3-node with two keys
        if self._is_red(node.left):
            if key < node.left.key:    direction, child = "left",  node.left.left
            elif key < node.key:       direction, child = "mid",   node.left.right
            else:                      direction, child = "right", node.right
        elif self._is_red(node.right):
            if key < node.key:         direction, child = "left",  node.left
            elif key < node.right.key: direction, child = "mid",   node.right.left
            else:                      direction, child = "right", node.right.right
        else: # Standard 2-node behavior
            direction = "left" if key < node.key else "right"
            child = node.left if direction == "left" else node.right

        # --- Leaf Insertion ---
        if child is None:
            new_node = self.RBNode(key, self.RED)
            if direction == "left":
                if self._is_red(node.left): node.left.left = new_node
                else: node.left = new_node
            elif direction == "right":
                if self._is_red(node.right): node.right.right = new_node
                else: node.right = new_node
            else: # direction == "mid"
                if self._is_red(node.left): node.left.right = new_node
                else: node.right.left = new_node
            return

        # --- Maintenance: 4-node Split ---
        if not self.is_4node(child):
            return self._insert_recursive(child, key)            

        # Now "mid" is reachable when the parent (node) is a 3-node
        if self.is_2node(node):
            if direction == "left": self.split_n4leftofn2(node)
            else: self.split_n4rightofn2(node)
        elif direction == "left":
            self.split_n4leftofn3(node)
        elif direction == "right":
            self.split_n4rightofn3(node)
        else: 
            self.split_n4midofn3(node) # REACHED!

        return self._insert_recursive(node, key)

    def search(self, key: int) -> bool:
        """Standard BST search - Simplicity First."""
        curr = self.root
        while curr:
            if key == curr.key:
                return True
            curr = curr.left if key < curr.key else curr.right
        return False

    def _fuse(self, parent: RBNode, child: RBNode, sibling: RBNode):
        """Surgical Change: Fuse a 2-node child with a 2-node sibling via color flips."""
        parent.color = self.BLACK
        child.color = self.RED
        if sibling:
            sibling.color = self.RED

    def delete(self, key: int):
        """Top-down 2-3-4 deletion logic using color swaps, no rotations."""
        if not self.root: return
        
        # Guard: Root must be treated as red to allow descent
        if self.is_2node(self.root):
            self.root.color = self.RED
            
        # Handle internal key at root before recursion
        if self.root.key == key:
            if not (self.root.left or self.root.right):
                self.root = None
                return
            else:
                successor_key = self._get_successor_key(self.root)
                self.root.key = successor_key
                self._delete_recursive(self.root, successor_key)
                if self.root: self.root.color = self.BLACK
                return

        self._delete_recursive(self.root, key)
        if self.root: self.root.color = self.BLACK

    def _delete_recursive(self, node, key):
        def _execute_remove_leaf(parent, direction):
            """Surgically nullify the correct pointer."""
            if direction == "left":
                if self._is_red(parent.left) and parent.left.key != key: 
                    parent.left.left = None
                else: parent.left = None
            elif direction == "right":
                if self._is_red(parent.right) and parent.right.key != key: 
                    parent.right.right = None
                else: parent.right = None
            elif direction == "mid":
                if self._is_red(parent.left): parent.left.right = None
                else: parent.right.left = None
        # ------------------------------------------------------------

        # --- Identification Logic: Target the actual node holding the key ---
        if self._is_red(node.left):
            if key < node.left.key:      direction, child, sibling = "left",  node.left.left, node.left.right
            elif key == node.left.key:   direction, child, sibling = "left",  node.left,       node.right # Target Red A
            elif key < node.key:         direction, child, sibling = "mid",   node.left.right, node.left.left
            else:                        direction, child, sibling = "right", node.right,      node.left
        elif self._is_red(node.right):
            if key < node.key:           direction, child, sibling = "left",  node.left,       node.right
            elif key < node.right.key:   direction, child, sibling = "mid",   node.right.left, node.right.right
            elif key == node.right.key:  direction, child, sibling = "right", node.right,      node.left # Target Red C
            else:                        direction, child, sibling = "right", node.right.right, node.right.left
        else:
            direction = "left" if key < node.key else "right"
            child = node.left if direction == "left" else node.right
            sibling = node.right if direction == "left" else node.left

        if child is None: return 

        # Maintenance: Upgrade 2-node child (standard 2-3-4)
        if self.is_2node(child) and (sibling is None or self.is_2node(sibling)):
            self._fuse(node, child, sibling)
            # After fusion, the structure changed; re-evaluate this level
            return self._delete_recursive(node, key)

        # --- Execution Logic ---
        if key == child.key:
            if not (child.left or child.right):
                _execute_remove_leaf(node, direction)
                return
            else:
                successor_key = self._get_successor_key(child)
                child.key = successor_key
                return self._delete_recursive(child, successor_key)

        return self._delete_recursive(child, key)

    def _get_successor_key(self, node):
        """Helper to find the leftmost key in the right subtree."""
        curr = node.right
        while curr.left: curr = curr.left
        return curr.key

    def inorder_iterator(self):
        """Yield keys in sorted (inorder) order. 234-tree style: ignore colors."""
        node = self.root
        stack = []
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.key
            node = node.right

    def print_inorder(self, sep=" "):
        """Print keys in sorted order on one line separated by `sep`."""
        first = True
        for k in self.inorder_iterator():
            if not first:
                sys.stdout.write(sep)
            sys.stdout.write(str(k))
            first = False
        sys.stdout.write("\n")

    def inorder_iterator(self):
        stack = []
        curr = self.root
        while curr or stack:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            yield curr.key
            curr = curr.right

if __name__ == "__main__":
    main()
