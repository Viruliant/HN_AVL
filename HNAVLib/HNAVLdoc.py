
from . import tree

def populateintoHNAVL(HNAVL):
    HNAVL.insert_path("HNAVL")

    HNAVL.insert_path("HNAVL/ListOps")
    HNAVL.insert_path("HNAVL/TreeOps")

############################################### List of List Operations:
    HNAVL.insert_path("HNAVL/ListOps/NewList")
    ## Create an empty list or initialize a list with
    ## provided values.
    HNAVL.insert_path("HNAVL/ListOps/Length")
    ## Return the number of nodes in the list.
    HNAVL.insert_path("HNAVL/ListOps/is_empty")
    ## Check if the list is empty: Determine if the list
    ## has any nodes. Uses Length().
    HNAVL.insert_path("HNAVL/ListOps/Search")
    ## Search for a given value (or range of values) in
    ## the list and return the nodes or their positions.
    HNAVL.insert_path("HNAVL/ListOps/Insert")
    ## Insert value at a specific position: Add value at
    ## a specified position in the list.
    HNAVL.insert_path("HNAVL/ListOps/Delete")
    ## Delete value at a specific position: Remove value
    ## at a specified position in the list and return it.
    HNAVL.insert_path("HNAVL/ListOps/SearchRange")
    ## Search for a given range of values in the list and
    ## return the nodes or their positions.
    HNAVL.insert_path("HNAVL/ListOps/InsertRange")
    ## Insert a range at a specific position: Add data at
    ## a specified position in the list.
    HNAVL.insert_path("HNAVL/ListOps/DeleteRange")
    ## Delete a range at a specific position: Remove data
    ## at a specified position and return the removed
    ## range.
    HNAVL.insert_path("HNAVL/ListOps/GetVals")
    ## Retrieve a range of values stored at a specified
    ## position.
    HNAVL.insert_path("HNAVL/ListOps/Update")
    ## Update value at a specific position: Modify the
    ## value stored in a node. Can be done with delete
    ## and insert.
    HNAVL.insert_path("HNAVL/ListOps/Concat")
    ## Combine two lists into a single list.
    HNAVL.insert_path("HNAVL/ListOps/Get_Start")
    ## Return the first node of the list. Uses GetVal().
    HNAVL.insert_path("HNAVL/ListOps/Get_End")
    ## Return the last node of the list. Uses GetVal().
    HNAVL.insert_path("HNAVL/ListOps/Reverse")
    ## Reverse the order of nodes in the list.
    HNAVL.insert_path("HNAVL/ListOps/Traverse")
    ## Traverse the list and perform an operation on each
    ## node.
    HNAVL.insert_path("HNAVL/ListOps/Iterate")
    ## Visit each node sequentially and perform a
    ## specific action.

## iterate() length() and insert() or delete() gives
## the following 5 functions:

    HNAVL.insert_path("HNAVL/ListOps/Insert_Start")
    ## Add a new node at the beginning of the list.
    HNAVL.insert_path("HNAVL/ListOps/Insert_End")
    ## Add a new node at the end of the list.
    HNAVL.insert_path("HNAVL/ListOps/Delete_Start")
    ## Remove the first node from the list.
    HNAVL.insert_path("HNAVL/ListOps/Delete_End")
    ## Remove the last node from the list.
    HNAVL.insert_path("HNAVL/ListOps/Print")
    ## Output the values stored in each node of the list.
    ## Can be done with iterate() and print char.

############################# List of Tree Operations:

    HNAVL.insert_path("HNAVL/TreeOps/Create")
    ## Create an empty tree or initialize a tree with a
    ## root node.
    HNAVL.insert_path("HNAVL/TreeOps/PreTraverse")
    ## Visit the nodes in the tree in pre-order (root,
    ## left subtree, right subtree) and perform an
    ## operation on each node.
    HNAVL.insert_path("HNAVL/TreeOps/InTraverse")
    ## Visit the nodes in the tree in in-order (left
    ## subtree, root, right subtree) and perform an
    ## operation on each node.
    HNAVL.insert_path("HNAVL/TreeOps/PostTraverse")
    ## Visit the nodes in the tree in post-order (left
    ## subtree, right subtree, root) and perform an
    ## operation on each node.
    HNAVL.insert_path("HNAVL/TreeOps/LevelTraverse")
    ## Visit the nodes in the tree level by level from top
    ## to bottom and perform an operation on each node.
    HNAVL.insert_path("HNAVL/TreeOps/Search")
    ## Search for a specific value or node in the tree and
    ## return the node or its position.
    HNAVL.insert_path("HNAVL/TreeOps/root")
    ## Return the root node of the tree.
    HNAVL.insert_path("HNAVL/TreeOps/parent")
    ## Return the parent node of a specified node.
    HNAVL.insert_path("HNAVL/TreeOps/child")
    ## Return the child nodes of a specified node.
    HNAVL.insert_path("HNAVL/TreeOps/number")
    ## Return the total number of nodes in the tree.
    HNAVL.insert_path("HNAVL/TreeOps/empty")
    ## Determine if the tree has any nodes.
    HNAVL.insert_path("HNAVL/TreeOps/InsertNode")
    ## Add a new node to the tree at a specified position.
    HNAVL.insert_path("HNAVL/TreeOps/InsertChild")
    ## Add a new child node to an existing parent node.
    HNAVL.insert_path("HNAVL/TreeOps/DeleteNode")
    ## Remove a specific node from the tree.
    HNAVL.insert_path("HNAVL/TreeOps/DeleteSubtree")
    ## Remove an entire subtree rooted at a specific node.
    HNAVL.insert_path("HNAVL/TreeOps/UpdateNode")
    ## Modify the value or properties of a specific node in the tree.
    HNAVL.insert_path("HNAVL/TreeOps/Copy")
    ## Create a copy of the entire tree.
    HNAVL.insert_path("HNAVL/TreeOps/Merge")
    ## Combine two trees into a single tree.
    HNAVL.insert_path("HNAVL/TreeOps/Prune")
    ## Remove specific nodes or subtrees from the tree.
    HNAVL.insert_path("HNAVL/TreeOps/Balance")
    ## Balance the tree: Perform operations to balance the
    ## tree, such as AVL rotations or red-black tree balancing.
    return HNAVL