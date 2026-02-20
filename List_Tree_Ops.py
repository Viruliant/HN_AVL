
############################################### List of List Operations:

        NewList() ## Create an empty list or initialize a list with
                  ## provided values.

         Length() ## Return the number of nodes in the list.

       is_empty() ## Check if the list is empty: Determine if the list
                  ## has any nodes. Uses Length().

         Search() ## Search for a given value (or range of values) in
                  ## the list and return the nodes or their positions.

         Insert() ## Insert value at a specific position: Add value at
                  ## a specified position in the list.

         Delete() ## Delete value at a specific position: Remove value
                  ## at a specified position in the list and return it.

    SearchRange() ## Search for a given range of values in the list and
                  ## return the nodes or their positions.

    InsertRange() ## Insert a range at a specific position: Add data at
                  ## a specified position in the list.

    DeleteRange() ## Delete a range at a specific position: Remove data
                  ## at a specified position and return the removed
                  ## range.

        GetVals() ## Retrieve a range of values stored at a specified
                  ## position.

         Update() ## Update value at a specific position: Modify the
                  ## value stored in a node. Can be done with delete
                  ## and insert.

         Update() ## Update value at a specific position: Modify the
                  ## value stored in a node. Can be done with delete
                  ## and insert.

         Concat() ## Combine two lists into a single list.

      Get_Start() ## Return the first node of the list. Uses GetVal().

        Get_End() ## Return the last node of the list. Uses GetVal().

        Reverse() ## Reverse the order of nodes in the list.

       Traverse() ## Traverse the list and perform an operation on each
                  ## node.

        Iterate() ## Visit each node sequentially and perform a
                  ## specific action.


## iterate() length() and insert() or delete() gives the following 5 functions:

   Insert_Start() ## Add a new node at the beginning of the list.
     Insert_End() ## Add a new node at the end of the list.
   Delete_Start() ## Remove the first node from the list.
     Delete_End() ## Remove the last node from the list.
          Print() ## Output the values stored in each node of the list.
                  ## Can be done with iterate() and print char.
          Print() ## Output the values stored in each node of the list.
                  ## Can be done with iterate() and print char.

############################################### List of Tree Operations:

         Create() ## Create an empty tree or initialize a tree with a
                  ## root node.

    PreTraverse() ## Visit the nodes in the tree in pre-order (root,
                  ## left subtree, right subtree) and perform an
                  ## operation on each node.

     InTraverse() ## Visit the nodes in the tree in in-order (left
                  ## subtree, root, right subtree) and perform an
                  ## operation on each node.

   PostTraverse() ## Visit the nodes in the tree in post-order (left
                  ## subtree, right subtree, root) and perform an
                  ## operation on each node.

  LevelTraverse() ## Visit the nodes in the tree level by level from top
                  ## to bottom and perform an operation on each node.

         Search() ## Search for a specific value or node in the tree and
                  ## return the node or its position.

           root() ## Return the root node of the tree.

         parent() ## Return the parent node of a specified node.

          child() ## Return the child nodes of a specified node.

         number() ## Return the total number of nodes in the tree.

          empty() ## Determine if the tree has any nodes.

     InsertNode() ## Add a new node to the tree at a specified position.

    InsertChild() ## Add a new child node to an existing parent node.

     DeleteNode() ## Remove a specific node from the tree.

  DeleteSubtree() ## Remove an entire subtree rooted at a specific node.

     UpdateNode() ## Modify the value or properties of a specific node in the tree.

           Copy() ## Create a copy of the entire tree.

          Merge() ## Combine two trees into a single tree.

          Prune() ## Remove specific nodes or subtrees from the tree.

        Balance() ## Balance the tree: Perform operations to balance the
                  ## tree, such as AVL rotations or red-black tree balancing.
