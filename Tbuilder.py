from collections import deque
from time import sleep
import json
import os
from typing import final

class Node:
    def __init__(self, val=0, childnodes=2) -> None:
        self.val = val
        self.childnodes = childnodes
        self.childs = [None] * childnodes
        self.txtformat = 'Node val: %s'
        for i in range(len(self.childs)):
            self.txtformat += f'\nPDchild_{i}: %s'

        if childnodes == 2:
            self.txtformat = self.txtformat.replace('child_0', 'left')
            self.txtformat = self.txtformat.replace('child_1', 'right')

    def __str__(self, i = 0) -> str:
        return self.txtformat.replace('PD', '\t'*(i+1)) % (self.val,  *[l.__str__(i+1) if l else l for l in self.childs])


class BaseTrees:

    def __init__(self, childnodes=2) -> None:
        self.node = Node(0, childnodes)

    def __str__(self) -> str:
        return self.printTree()

    def printTree(self) -> str:
        root = self.node
        depth = 0
        def finddepth(root,d):
            if root:
                nonlocal depth
                depth = max(depth,d)
                finddepth(root.childs[0],d+1)
                finddepth(root.childs[1],d+1)
        
        def solve(root, x, y):
            if root:
                matrix[x][y] = str(root.val)
                solve(root.childs[0],x+1,y-2**(depth-x-1))
                solve(root.childs[1],x+1,y+2**(depth-x-1))
        
        finalTree = ""
        
        finddepth(root,0)
        matrix = [[' ' for _ in range(2**(depth+1)-1)] for y in range(depth+1)]
        solve(root,0,len(matrix[0])//2)
        for line in range(len(matrix)):
            finalTree+=f'{line}:'
            for j in matrix[line]:
                finalTree+=j
            finalTree+='\n'

        return finalTree
        
    def buildfromtamplate(self, template) -> None:
        self.node.val = template.pop(0)      
        queue = deque([self.node])

        while queue:
            nd = queue.popleft()
            i = 0
            while i < self.node.childnodes and i < len(template):
                nd.childs[i] = Node(template[i], self.node.childnodes)
                queue.append(nd.childs[i])
                i+=1
            template = template[i:]
        return self.node
    
    def makejson(self, node = None) -> None:
        def makedict(node):
            if not node:
                return None
            js = {"Val":node.val} | {"children" : {"child_" + str(i) : makedict(node.childs[i]) for i in range(len(node.childs))}}

            return js
        dc = makedict(self.node)
        i = 0

        while True:
            if (path:='yourtree{}.json'.format(i)) not in os.listdir():
                with open(path, 'w') as f:    
                    f.write(json.dumps(dc, indent=4))
                    return
            i+=1

class BSTree(BaseTrees):

    def __getmax(self, node):
        return self.__getmax(node.childs[1]) if node.childs[1] else node

    def getmax(self, node=None):
        return self.__getmax(node if node else self.node)

    def __isub__(self, value):
        def delete(node, previous):
            
            if node:
                if node.val == value:
                    if not node.childs[0]:
                        previous.childs[value > previous.val] = node.childs[1]
                    elif not node.childs[1]:
                        previous.childs[value > previous.val] = node.childs[0]
                    else:
                        newval = self.getmax(node.childs[0])
                        self.__isub__(newval.val)
                        previous.childs[value > previous.val].val = newval.val
                
                delete(node.childs[value > previous.val], node)

        fakeroot = Node(-1, 2)
        fakeroot.childs[1] = self.node
        delete(self.node, fakeroot)
        return self

    def __iadd__(self, value):
        
        def insert(node):
            if not node:
                return True
            if value > node.val:
                l = insert(node.childs[1])
            else:
                l = insert(node.childs[0])

            if l:
                node.childs[value >= node.val] = Node(value, 2)


        insert(self.node)
        return self



if __name__ == '__main__':
    btr = BSTree(2)
    btr.buildfromtamplate([4,2,7,1,3])
    
    
    
