import random
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

class GraphNode:
    def __init__(self, key):
        self.key = key
        self.parents = []
        self.children = []
        self.visited = False

    def __str__(self):
        return str({
            'key': self.key,
            'children': str([c.key for c in self.children]),
            'parents' : str([c.key for c in self.parents]),
            'visited': self.visited
        })

    def add_child(self, node):
        self.children.append(node)
        node.parents.append(self)
    
    def remove_child(self, node):
        node.parents.remove(self)
        self.children.remove(node)
        

    @staticmethod
    def plot_graph(adj):
        G = nx.DiGraph(adj)
        nx.draw_networkx(G)
        plt.show()  

    @staticmethod
    def dict_to_graph(d):
        nodes = {}
        for key in d.keys():
            nodes[key] = GraphNode(key)
        
        for key in d.keys():
            for n in d[key]:
                nodes[key].children.append(nodes[n])
        return list(nodes.values())[0]

class TreeNode:

    def __init__(self, key):
        self.key = key
        self.right = None
        self.left = None
        self.parent = None

    def __str__(self):
        return str({
            'key': self.key,
            'left_key': self.left.key if self.left != None else None,
            'right_key': self.right.key if self.right != None else None,
            'parent_key': self.parent.key if self.parent != None else None
        })

    def insert(self, key):
        if self.key == key:
            return
        elif self.key < key:
            if self.right is None:
                self.right = TreeNode(key)
            else:
                self.right.insert(key)
            self.right.parent = self
        else: # self.key > key
            if self.left is None:
                self.left = TreeNode(key)
            else:
                self.left.insert(key)
            self.left.parent = self

    @staticmethod
    def get_random_node(root, maxsteps = 10):
        curr = root
        steps = random.randint(1, maxsteps)
        for i in range(0, steps):
            go_left = random.randint(0, 1) == 0 and curr.left != None
            if go_left:
                curr = curr.left
            elif curr.right != None:
                curr = curr.right
            else:
                break
        return curr
            
    @staticmethod
    def random_tree(n, min=0, max=100):
        root = TreeNode(random.randint(min, max))
        node = root
        for _ in range(n-1):
            insert_left = random.randint(0, 1) == 0
            value = random.randint(min, max)
            if insert_left: 
                if node.left != None: node = node.left
                node.left = TreeNode(value)
                if node.right != None: node = node.left
            else:
                if node.right != None: node = node.right
                node.right = TreeNode(value)
                if node.left != None: node = node.right
        return root


    @staticmethod
    def random_bst(n, min=0, max=100):
        b = TreeNode(random.randint(min, max))
        for _ in range(n-1):
            b.insert(random.randint(min, max))
        return b

    @staticmethod
    def random_balanced_bst(n, min=0, max=100):
        node = TreeNode.random_bst(n, min, max)
        return TreeNode.balanced_bst(node)

    @staticmethod
    def balanced_bst(node):    
        arr = []
        TreeNode.in_order_traversal(node,arr)
        return TreeNode.balanced_bst_from_list(arr)

    @staticmethod
    def balanced_bst_from_list(arr):
        if not arr: return None

        # get middle node
        mid = len(arr) // 2
        root = TreeNode(arr[mid])

        # recursively get left and right half of tree
        root.left = TreeNode.balanced_bst_from_list(arr[0:mid])
        root.right = TreeNode.balanced_bst_from_list(arr[mid+1:])

        return root

    # In-order traversal means to "visit" (often, print) the left branch, then the current node, and finally, the right branch.
    @staticmethod
    def in_order_traversal(node, results=[]):
        #if len(results) == 0: results.append(node.key)
        if node == None: return
        TreeNode.in_order_traversal(node.left, results)
        results.append(node.key)
        TreeNode.in_order_traversal(node.right, results)

    # Pre-order traversal visits the current node before its child nodes (hence the name "pre-order").
    @staticmethod
    def pre_order_traversal(node, results=[]):
        if node == None: return
        results.append(node.key)
        TreeNode.pre_order_traversal(node.left, results)
        TreeNode.pre_order_traversal(node.right, results)

    # Post-order traversal visits the current node after its child nodes (hence the name "post-order").
    @staticmethod
    def post_order_traversal(node, results=[]):
        if node == None: return
        TreeNode.post_order_traversal(node.left, results)
        TreeNode.post_order_traversal(node.right, results)

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.key
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

# https://www.askpython.com/python/examples/min-heap

def build_min_heap(arr):
    nodes = [TreeNode(arr[i]) for i in range(1,len(arr))]
    nodes = list(filter(lambda n: n.key != None, nodes))
    maxsize = len(arr)
    nodes.insert(0,None)
    cursize = len(nodes) - 1
    node = None
    for i in range(cursize//2, 0, -1):
        # create node
        node = nodes[i]

        # get child indeces (1-based)
        ileft = 2*i
        iright = 2*i + 1

        # set childrend
        if ileft <= cursize: node.left = nodes[ileft]
        if iright <= cursize: node.right = nodes[iright]
    return node





