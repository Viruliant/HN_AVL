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
# SEQ_AVL_test.py
# sequential AVL tree

import subprocess, threading, re, os, sys, inspect, shutil, argparse, random, math, fnmatch, json, types

def main():
    test_int32_sequence()
    test_uint8_sequence()

INT32_MASK = 0xFFFFFFFF

def int32(x: int) -> int:
    x &= INT32_MASK
    return x if x < 0x80000000 else x - 0x100000000

def uint8(x: int) -> int:
    """Cast to unsigned 8-bit integer (0..255)."""
    return int(x) & 0xFF

class SEQ_AVL:
    def __init__(self, cast_fn=None):
        """
        cast_fn: optional function applied to every key on node creation.
                 Pass int32 to enforce 32-bit signed integers,
                 pass uint8 to enforce 8-bit unsigned integers, or None for no casting.
        """
        self.root = None
        self.cast_fn = cast_fn

    class Node:
        def __init__(self, key, cast_fn=None):
            self.key = cast_fn(key) if cast_fn else key
            self.left = None
            self.right = None
            self.height = 1
            self.size = 1

    def _height(self, n):
        return 0 if not n else n.height

    def _size(self, n):
        return 0 if not n else n.size

    def _update(self, n):
        if not n:
            return None
        n.height = 1 + max(self._height(n.left), self._height(n.right))
        n.size = 1 + self._size(n.left) + self._size(n.right)
        return n

    def _rebalance(self, node):
        def _balance(n):
            return self._height(n.left) - self._height(n.right) if n else 0
        def rotate_left(x):
            y = x.right
            x.right = y.left
            y.left = x
            self._update(x)
            self._update(y)
            return y
        def rotate_right(y):
            x = y.left
            y.left = x.right
            x.right = y
            self._update(y)
            self._update(x)
            return x
        if not node:
            return None
        bf = _balance(node)
        if bf > 1:
            if _balance(node.left) < 0:
                node.left = rotate_left(node.left)
            return rotate_right(node)
        if bf < -1:
            if _balance(node.right) > 0:
                node.right = rotate_right(node.right)
            return rotate_left(node)
        return node

    def search(self, index: int):
        node = self.root
        curr_idx = index
        while node:
            left_size = self._size(node.left)
            if curr_idx < left_size:
                node = node.left
            elif curr_idx == left_size:
                return node
            else:
                curr_idx -= (left_size + 1)
                node = node.right
        return None

    def insert(self, index: int, key):
        def _insert_at_index(node, index, key):
            if not node:
                return SEQ_AVL.Node(key, self.cast_fn)
            left_size = self._size(node.left)
            if index <= left_size:
                node.left = _insert_at_index(node.left, index, key)
            else:
                node.right = _insert_at_index(node.right, index - left_size - 1, key)
            self._update(node)
            return self._rebalance(node)
        curr_size = self._size(self.root)
        target_idx = max(0, min(index, curr_size))
        self.root = _insert_at_index(self.root, target_idx, key)
        return self.root

    def delete(self, index: int):
        def _delete_at_index(node, idx):
            if not node:
                return None
            left_size = self._size(node.left)
            if idx < left_size:
                node.left = _delete_at_index(node.left, idx)
            elif idx > left_size:
                node.right = _delete_at_index(node.right, idx - left_size - 1)
            else:
                if not node.left:
                    return node.right
                if not node.right:
                    return node.left
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.key = succ.key
                node.right = _delete_at_index(node.right, 0)
            self._update(node)
            return self._rebalance(node)
        if 0 <= index < self._size(self.root):
            self.root = _delete_at_index(self.root, index)
        return self.root

    def inorder(self, func):
        """In-order traversal: applies the provided function (e.g. printchar)
        to each key in sequence order (left-key-right)."""
        def _inorder(node):
            if node:
                _inorder(node.left)
                func(node.key)
                _inorder(node.right)
        _inorder(self.root)

    def preorder(self, func):
        """General preorder traversal that provides structural metadata to the callback."""
        def _visit(node, prefix, is_last):
            if not node:
                return
            # Pass the node and its structural context to the callback
            func(node, prefix, is_last)
            # Calculate the prefix for the next level
            new_prefix = prefix + ("    " if is_last else "│   ")
            # Determine children and which one is 'last'
            has_left = node.left is not None
            has_right = node.right is not None
            if has_left:
                # Left is 'last' only if there is no right sibling
                _visit(node.left, new_prefix, not has_right)
            if has_right:
                # Right is always 'last' in a binary tree preorder
                _visit(node.right, new_prefix, True)
        _visit(self.root, "", True)

###########################
# Utility functions / tests

def format_key(key: int) -> str:
    """Converts key to Unicode char if valid, else returns hex string."""
    try:
        if isinstance(key, int) and 0 <= key <= 0x10FFFF:
            return f"{hex(key)} ('{chr(key)}')"
        if isinstance(key, int):
            return f"{hex(key)} (Out of Unicode Range)"
        return repr(key)
    except Exception:
        return repr(key)

def codepoint_to_char(key) -> str:
    """Convert a possibly-signed 32-bit code point to a printable character.
    Valid Unicode → actual char; everything else → escape (never crashes)."""
    if not isinstance(key, int):
        return repr(key)
    cp = key & 0xFFFFFFFF  # treat as unsigned 32-bit
    if 0 <= cp <= 0x10FFFF:
        ch = chr(cp)
        return ch if ch.isprintable() else f"U+{cp:04X}"
    return f"\\U{cp:08X}"

def standalone_print_tree(node, prefix, is_last):
    """Replacement for the internal print_tree method."""
    char_rep = codepoint_to_char(node.key)
    display_str = f"'{char_rep}' (sz:{node.size})"
    connector = "└── " if is_last else "├── "
    print(prefix + connector + display_str)

def load_rand_seq(tree, n: int, valid_ranges=None):
    """Insert n random keys into random positions in the tree.
    valid_ranges: iterable of integer keys to choose from. If None, defaults to 0x30-0x39 and 0x41-0x46."""
    print(f"\n--- Loading {n} random chars into random positions ---")
    if valid_ranges is None:
        valid_ranges = list(range(0x30, 0x39 + 1)) + list(range(0x41, 0x46 + 1))
    valid_ranges = list(valid_ranges)
    for _ in range(n):
        key = random.choice(valid_ranges)
        curr_size = tree._size(tree.root)
        pos = random.randint(0, curr_size)
        tree.insert(pos, key)

def delete_rand_seq(tree, k: int):
    """Delete k nodes from random valid indices."""
    print(f"\n--- Deleting {k} random indices ---")
    for _ in range(k):
        curr_size = tree._size(tree.root)
        if curr_size == 0:
            return
        idx = random.randrange(curr_size)
        target_node = tree.search(idx)
        if not target_node:
            continue
        target_key = target_node.key
        tree.delete(idx)
        # Verification: Size should decrement
        assert tree._size(tree.root) == curr_size - 1

def test_int32_sequence():
    print("=== int32 sequence test ===")
    random.seed(42)
    t = SEQ_AVL(cast_fn=int32)
    load_rand_seq(t, 100)
    print(f"Sequence after load (int32 as printable chars): ")
    t.inorder(lambda k: print(codepoint_to_char(k), end=''))
    delete_rand_seq(t, 80)
    print(f"Final Sequence (int32): ")
    t.inorder(lambda k: print(codepoint_to_char(k), end=''))
    print()
    t.preorder(standalone_print_tree)

def test_uint8_sequence():
    print("\n=== uint8 sequence test ===")
    random.seed(123)
    # For uint8 test, use full byte range 0..255
    t = SEQ_AVL(cast_fn=uint8)
    load_rand_seq(t, 50, valid_ranges=range(0, 255))
    print(f"\nSequence after load (uint8 hex): ")
    t.inorder(lambda k: print(f"{k & 0xFF:02X}", end=' '))
    # Delete some random bytes
    delete_rand_seq(t, 30)
    print(f"Final Sequence (uint8 hex): ", end='')
    t.inorder(lambda k: print(f"{k & 0xFF:02X}", end=' '))

if __name__ == "__main__":
    main()
