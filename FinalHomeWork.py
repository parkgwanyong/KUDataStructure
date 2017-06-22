class Node:
    def __init__(self, newval):
        self.parent = None
        self.key = newval
        self.left = None
        self.right = None
        self.red = True
        self.black = False
class NilNode:
    def __init__(self):
        self.parent = None
        self.key = None
        self.left = None
        self.right = None
        self.red = False


class RedBlackTree:
    def __init__(self):
        self.root = nilnode

    def search(self,key):
        node = self.root
        while node !=nilnode and node.key != key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node

    def nearsearch(self,key):
        node = self.root
        nearnode = self.root
        diff = self.maximum(self.root).key
        while node !=nilnode and nearnode.key != key:
            if key < node.key:
                if abs(node.key-key) < diff:
                    diff = abs(node.key-key)
                    nearnode = node
                node = node.left
            else:
                if abs(node.key - key) < diff:
                    diff = abs(node.key - key)
                    nearnode = node
                node = node.right
        return nearnode

    def RBInsert(self,z):
        y = nilnode
        x = self.root
        while x != nilnode:
            y = x
            if z.key < x.key:
                x = x.left
            else: x = x.right
        z.parent = y
        if y == nilnode:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else: y.right = z
        z.left = nilnode
        z.right = nilnode
        z.red = True
        self.RBInsertFixUp(z)

    def RBInsertFixUp(self,z):

        while  z.parent.red == True:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.red ==True:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                    continue
                elif z==z.parent.right:
                    z = z.parent
                    self.LeftRotate(z)
                z.parent.red = False
                z.parent.parent.red = True
                self.RightRotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if  y.red == True:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                    continue
                elif z == z.parent.left:
                    z = z.parent
                    self.RightRotate(z)
                z.parent.red = False
                z.parent.parent.red = True
                self.LeftRotate(z.parent.parent)
        self.root.red = False

    def LeftRotate(self,x):
        y = x.right
        x.right = y.left
        if y.left != nilnode:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == nilnode:
            self.root = y
        elif x==x.parent.left:
            x.parent.left = y
        else: x.parent.right = y
        y.left = x
        x.parent = y

    def RightRotate(self,x):
        y = x.left
        x.left = y.right
        if y.right != nilnode:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == nilnode:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def inorder_walk(self):
        inorderarr = []
        val = self.minimum(self.root)
        while val !=nilnode:
            inorderarr.append(val)
            val = self.successor(val)
        return inorderarr

    def minimum(self, x):
        while x.left != nilnode:
            x = x.left
        return x

    def maximum(self, x):
        while x.right != nilnode:
            x = x.right
        return x

    def successor(self, x):
        if x.right != nilnode:
            return self.minimum(x.right)
        y = x.parent
        while y !=nilnode and x==y.right:
            x=y
            y=y.parent
        return y


    def predecessor(self,x):
        if x.left !=nilnode:
            return self.maximum(x.left)
        y = x.parent
        while y!=nilnode and x==y.left:
            x = y
            y = y.parent
        return y

    def RBDelete(self,z):
        y = z
        y_original_color = y.red
        if z.left == nilnode:
            x = z.right
            self.RBTransplant(z,z.right)
        elif z.right == nilnode:
            x = z.left
            self.RBTransplant(z,z.left)
        else:
            y = self.minimum(z.right)
            x = y.right
            if y.parent ==z:
                x.parent = y
            else:
                self.RBTransplant(y,y.right)
                y.right = z.right
                y.right.parent = y
            self.RBTransplant(z,y)
            y.left = z.left
            y.left.parent = y
            y.red = z.red
        if y_original_color == False:
            self.RBDeleteFixUp(x)


    def RBTransplant(self,u,v):
        if u.parent == nilnode:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:u.parent.right = v
        v.parent = u.parent

    def RBDeleteFixUp(self,x):
        while x != self.root and x.red ==False and x !=nilnode:
            if x == x.parent.left:
                w = x.parent.right
                if w.red == True:
                    w.red = False
                    x.parent.red = True
                    self.LeftRotate(x.parent)
                    w = x.parent.right
                if w.left.red == False and w.right.red == False:
                    w.red = True
                    x = x.parent
                    continue
                elif w.right.red == False:
                    w.left.red = False
                    w.red = True
                    self.RightRotate(w)
                    w = x.parent.right
                    w.red = x.parend.red
                    x.parent.red = False
                    w.right.red = False
                    self.LeftRotate(x.p)
                    x=self.root
                else:
                    w = x.p.left
                    if w.red == True:
                        w.red = False
                        x.parent.red = True
                        self.RightRotate(x.parent)
                        w = x.parent.left
                    if w.right.red == False and w.left.red == False:
                        w.red = True
                        x = x.parent
                        continue
                    elif w.left.red == False:
                        w.right.red = False
                        w.red = True
                        self.LeftRotate(w)
                        w = x.parent.left
                        w.red = x.parend.red
                        x.parent.red = False
                        w.left.red = False
                        self.RightRotate(x.p)
                        x = self.root
        x.red = False



nilnode = NilNode()
def main():
    f = open("input.txt", 'r')
    tmpdata = f.read()
    data = tmpdata.split()
    f.close()
    tree = RedBlackTree()

    g = open("search.txt", 'r')
    tmpdata2 = g.read()
    data2 = tmpdata2.split()
    g.close()

    w = open("output.txt", 'w')

    for i in data:
        if int(i) > 0:
            tree.RBInsert(Node(int(i)))
        elif int(i) <0:
            findnode = tree.search(abs(int(i)))

            tree.RBDelete(findnode)
        else:
            break

    for j in data2:
        if j !="0":
            node = tree.search(int(j))
            nrnode = tree.nearsearch(int(j))

            if int(j) < nrnode.key:
                nxtnode = nrnode
                prenode = tree.predecessor(nrnode)
            elif int(j) > nrnode.key:
                nxtnode = tree.successor(nrnode)
                prenode = nrnode
            else:
                nxtnode = tree.successor(nrnode)
                prenode = tree.predecessor(nrnode)

            if prenode.key == None:
                printprenode = "NIL"
            else:
                printprenode = prenode.key
            if nxtnode.key == None:
                printnxtnode = "NIL"
            else:
                printnxtnode = nxtnode.key

            if node.key == None:
                printnode = "NIL"
            else:
                printnode = node.key

            sentence = str(printprenode) + " " + str(printnode) + " " + str(printnxtnode) + "\n"
            w.write(sentence)
    w.close()




main()
