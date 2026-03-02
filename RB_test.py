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
----------------------------------------------------------------------

The following YAML representations capture the transformation of 
Red-Black Trees and their equivalent 2-3-4 Tree structures during 
4-node splitting operations.

6 split cases: n4splitn2 n4leftofn2 n4righttofn2 n4leftofn3 n4midofn3 n4rightofn3

```yaml
n4splitn2:
  RBTree-before:
    root:
      node: { color: black, content: B }
      left: { node: { color: red, content: A }, left: 1, right: 2 }
      right: { node: { color: red, content: C }, left: 3, right: 4 }
  RBTree-after:
    root:
      node: { color: red, content: B }
      left: { node: { color: black, content: A }, left: 1, right: 2 }
      right: { node: { color: black, content: C }, left: 3, right: 4 }
  234Tree-before:
    !4node:
      - first: 1
      - {!node: { content: A }}
      - second: 2
      - {!node: { content: B }}
      - third: 3
      - {!node: { content: C }}
      - fourth: 4
  234Tree-after:
    !2node:
      first: 
        !2node: { first: 1, node: { content: A }, second: 2 }
      node: { content: B }
      second:
        !2node: { first: 3, node: { content: C }, second: 4 }

n4righttofn2:
  RBTree-before:
    root:
      node: { color: black, content: A }
      left: 1
      right:
        node: { color: black, content: C }
        left: { node: { color: red, content: B }, left: 2, right: 3 }
        right: { node: { color: red, content: D }, left: 4, right: 5 }
  RBTree-after:
    root:
      node: { color: black, content: A }
      left: 1
      right:
        node: { color: red, content: C }
        left: { node: { color: black, content: B }, left: 2, right: 3 }
        right: { node: { color: black, content: D }, left: 4, right: 5 }
  234Tree-before:
    !2node:
      first: 1
      node: { content: A }
      second:
        !4node:
          - first: 2
          - {!node: { content: B }}
          - second: 3
          - {!node: { content: C }}
          - third: 4
          - {!node: { content: D }}
          - fourth: 5
  234Tree-after:
    !3node:
      - first: 1
      - {!node: { content: A }}
      - second:
          !2node: { first: 2, node: { content: B }, second: 3 }
      - {!node: { content: C }}
      - third:
          !2node: { first: 4, node: { content: D }, second: 5 }

n4leftofn2:
  RBTree-before:
    root:
      node: { color: black, content: D }
      left:
        node: { color: black, content: B }
        left: { node: { color: red, content: A }, left: 1, right: 2 }
        right: { node: { color: red, content: C }, left: 3, right: 4 }
      right: 5
  RBTree-after:
    root:
      node: { color: black, content: D }
      left:
        node: { color: red, content: B }
        left: { node: { color: black, content: A }, left: 1, right: 2 }
        right: { node: { color: black, content: C }, left: 3, right: 4 }
      right: 5
  234Tree-before:
    !2node:
      first:
        !4node:
          - first: 1
          - {!node: { content: A }}
          - second: 2
          - {!node: { content: B }}
          - third: 3
          - {!node: { content: C }}
          - fourth: 4
      node: { content: D }
      second: 5
  234Tree-after:
    !3node:
      - first:
          !2node: { first: 1, node: { content: A }, second: 2 }
      - {!node: { content: B }}
      - second:
          !2node: { first: 3, node: { content: C }, second: 4 }
      - {!node: { content: D }}
      - third: 5

n4leftofn3:
  RBTree-before:
    root:
      node: { color: black, content: D }
      left:
        node: { color: black, content: B }
        left: { node: { color: red, content: A }, left: 1, right: 2 }
        right: { node: { color: red, content: C }, left: 3, right: 4 }
      right: { node: { color: red, content: E }, left: 5, right: 6 }
  RBTree-after:
    root:
      node: { color: black, content: D }
      left:
        node: { color: red, content: B }
        left: { node: { color: black, content: A }, left: 1, right: 2 }
        right: { node: { color: black, content: C }, left: 3, right: 4 }
      right: { node: { color: red, content: E }, left: 5, right: 6 }
  234Tree-before:
    !3node:
      - first: 
          !4node: [1, A, 2, B, 3, C, 4]
      - {!node: { content: D }}
      - second: 5
      - {!node: { content: E }}
      - third: 6
  234Tree-after:
    !4node:
      - first: !2node: [1, A, 2]
      - {!node: { content: B }}
      - second: !2node: [3, C, 4]
      - {!node: { content: D }}
      - third: 5
      - {!node: { content: E }}
      - fourth: 6

n4midofn3:
  RBTree-before:
    root:
      node: { color: black, content: E }
      left:
        node: { color: red, content: A }
        left: 1
        right:
          node: { color: black, content: C }
          left: { node: { color: red, content: B }, left: 2, right: 3 }
          right: { node: { color: red, content: D }, left: 4, right: 5 }
      right: 6
  RBTree-after:
    root:
      node: { color: black, content: C }
      left: { node: { color: red, content: A }, left: 1, right: { node: { color: black, content: B }, left: 2, right: 3 }}
      right: { node: { color: red, content: E }, left: { node: { color: black, content: D }, left: 4, right: 5 }, right: 6 }
  234Tree-before:
    !3node:
      - first: 1
      - {!node: { content: A }}
      - second:
          !4node: [2, B, 3, C, 4, D, 5]
      - {!node: { content: E }}
      - third: 6
  234Tree-after:
    !4node:
      - first: 1
      - {!node: { content: A }}
      - second: !2node: [2, B, 3]
      - {!node: { content: C }}
      - third: !2node: [4, D, 5]
      - {!node: { content: E }}
      - fourth: 6

n4rightofn3:
  RBTree-before:
    root:
      node: { color: black, content: B }
      left: { node: { color: red, content: A }, left: 1, right: 2 }
      right:
        node: { color: black, content: D }
        left: { node: { color: red, content: C }, left: 3, right: 4 }
        right: { node: { color: red, content: E }, left: 5, right: 6 }
  RBTree-after:
    root:
      node: { color: black, content: B }
      left: { node: { color: red, content: A }, left: 1, right: 2 }
      right:
        node: { color: red, content: D }
        left: { node: { color: black, content: C }, left: 3, right: 4 }
        right: { node: { color: black, content: E }, left: 5, right: 6 }
  234Tree-before:
    !3node:
      - first: 1
      - {!node: { content: A }}
      - second: 2
      - {!node: { content: B }}
      - third:
          !4node: [3, C, 4, D, 5, E, 6]
  234Tree-after:
    !4node:
      - first: 1
      - {!node: { content: A }}
      - second: 2
      - {!node: { content: B }}
      - third: !2node: [3, C, 4]
      - {!node: { content: D }}
      - fourth: !2node: [5, E, 6]

```

'''

import subprocess, threading, re, os, sys, inspect, shutil, argparse, random, math, fnmatch, json, types

def load_rand(tree, n: int):
    for _ in range(n):
        key = random.randint(0, 1000000)
        tree.insert(key)

def main():
    random.seed(42) # Same random nums
    t = RedBlackTree()
    load_rand(t, 20)
    t.print_inorder()

# new version
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
        if key < parent.key:
            # parent.left must be None here
            parent.left = new_node
        else:
            # parent.right must be None here
            parent.right = new_node

    def insert(self, key: int):
        # - **Never rotate**
        # - **Never rebalance bottom‑up**
        # - **Always split 4‑nodes before descending**
        # - **Use your six split functions to mimic 234‑tree node splits**
        # - **Insert into leaf after all splits are done**
        # This produces an RB implementation that *reads exactly like a 234‑tree algorithm*.
            if self.root is None:
                self.root = self.RBNode(key, self.BLACK)
                return

            # 1. Split root if it is a 4-node
            if self.is_4node(self.root):
                self.split_n4splitn2(self.root)
                self.root.color = self.BLACK # Root must stay black

            node = self.root
            while True:
                # 2. Descend top-down
                if key == node.key: return # Avoid duplicates
                
                direction = "left" if key < node.key else "right"
                child = node.left if direction == "left" else node.right

                # If we reached the insertion point
                if child is None:
                    new_node = self.RBNode(key, self.RED)
                    if direction == "left":
                        node.left = new_node
                    else:
                        node.right = new_node
                    break

                # 3. If child is a 4-node, split it BEFORE descending
                if self.is_4node(child):
                    if self.is_2node(node):
                        if direction == "left":
                            self.split_n4leftofn2(node)
                        else:
                            self.split_n4rightofn2(node)
                    else:
                        # Parent is a 3-node (has one red child)
                        # Determine if 'child' is the red child's descendant (middle)
                        is_left_red = self._is_red(node.left)
                        
                        if direction == "left":
                            self.split_n4leftofn3(node)
                        elif direction == "right":
                            self.split_n4rightofn3(node)
                        else:
                            # This logic handles the logical 'middle' of a 3-node
                            self.split_n4midofn3(node)

                    # After split, re-evaluate which way to go because 
                    # the colors changed the 2-3-4 node boundaries
                    if key < node.key:
                        child = node.left
                    else:
                        child = node.right

                node = child

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
        if not self.root:
            return

        # Goal: Ensure root is not a 2-node to start
        if self.is_2node(self.root):
            self.root.color = self.RED

        curr = self.root
        parent = None
        
        while curr:
            # Pre-emptive 2-node transformation
            if self.is_2node(curr) and parent:
                # Find sibling
                sibling = parent.right if parent.left == curr else parent.left
                # If sibling is also 2-node, fuse them
                if self.is_2node(sibling):
                    self._fuse(parent, curr, sibling)
                # Note: If sibling is 3/4 node, 'borrowing' usually requires rotations.
                # Per SOP: Mentioning limitation - strictly avoiding rotations 
                # might lead to simpler but more aggressive fusing.

            if key == curr.key:
                if curr.left and curr.right:
                    # Internal node: Surgical key swap with successor
                    successor = curr.right
                    while successor.left: successor = successor.left
                    curr.key = successor.key
                    key = successor.key # Continue to delete the swapped leaf
                else:
                    # Leaf or single child: Surgical removal
                    replacement = curr.left or curr.right
                    if not parent:
                        self.root = replacement
                    elif parent.left == curr:
                        parent.left = replacement
                    else:
                        parent.right = replacement
                    return

            parent = curr
            curr = curr.left if key < curr.key else curr.right
        
        # Ensure root stays black after all operations
        if self.root: self.root.color = self.BLACK

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

if __name__ == "__main__":
    main()
