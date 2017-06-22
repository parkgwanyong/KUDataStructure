

class Node:
    Red = True
    Black = False

    def __init__(self, key, color=Red):
        self.color = color
        self.key = key
        self.left = self.right = self.parent = NilNode.instance()

    def __nonzero__(self):
        return True

    def __bool__(self):
        return True


class NilNode(Node):
    __instance__ = None

    @classmethod
    def instance(self):
        if self.__instance__ is None:
            self.__instance__ = NilNode()
        return self.__instance__

    def __init__(self):
        self.color = Node.Black
        self.key = None
        self.left = self.right = self.parent = None

    def __nonzero__(self):
        return False

    def __bool__(self):
        return False


class RedBlackTree:
    def __init__(self):
        self.root = NilNode.instance()
        self.size = 0

    def insert(self, InsertNode):
        self.insert_fixup(InsertNode)

        InsertNode.color = Node.Red
        while InsertNode != self.root and InsertNode.parent.color == Node.Red:
            if InsertNode.parent == InsertNode.parent.parent.left:
                y = InsertNode.parent.parent.right
                if y and y.color == Node.Red:
                    InsertNode.parent.color = Node.Black
                    y.color = Node.Black
                    InsertNode.parent.parent.color = Node.Red
                    InsertNode = InsertNode.parent.parent
                else:
                    if InsertNode == InsertNode.parent.right:
                        InsertNode = InsertNode.parent
                        self.left_rotate(InsertNode)
                    InsertNode.parent.color = Node.Black
                    InsertNode.parent.parent.color = Node.Red
                    self.right_rotate(InsertNode.parent.parent)
            else:
                y = InsertNode.parent.parent.left
                if y and y.color == Node.Red:
                    InsertNode.parent.color = Node.Black
                    y.color = Node.Black
                    InsertNode.parent.parent.color = Node.Red
                    InsertNode = InsertNode.parent.parent
                else:
                    if InsertNode == InsertNode.parent.left:
                        InsertNode = InsertNode.parent
                        self.right_rotate(InsertNode)
                    InsertNode.parent.color = Node.Black
                    InsertNode.parent.parent.color = Node.Red
                    self.left_rotate(InsertNode.parent.parent)
        self.root.color = Node.Black

    def insert_fixup(self, FixupNode):
        TmpNode = NilNode.instance()
        CheckNode = self.root
        while CheckNode:
            TmpNode = CheckNode
            if FixupNode.key < CheckNode.key:
                CheckNode = CheckNode.left
            else:
                CheckNode = CheckNode.right

        FixupNode.parent = TmpNode
        if not TmpNode:
            self.root = FixupNode
        else:
            if FixupNode.key < TmpNode.key:
                TmpNode.left = FixupNode
            else:
                TmpNode.right = FixupNode
        self.size += 1

    def delete(self, z):
        if not z.left or not z.right:
            y = z
        else:
            y = self.successor(z)
        if not y.left:
            x = y.right
        else:
            x = y.left
        if x is None:
            return
        x.parent = y.parent

        if not y.parent:
            self.root = x
        else:
            if y == y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x

        if y != z: z.key = y.key

        if y.color == Node.Black:
            self.delete_fixup(x)

        self.size -= 1
        return y

    def minimum(self, min=None):
        if min is None: min = self.root
        while min.left:
            min = min.left
        return min
    def maximum(self, max=None):
        if max is None: max = self.root
        while max.right:
            max = max.right
        return max

    def successor(self, current):
        if current.right:
            return self.minimum(current.right)
        successor = current.parent
        while successor and current == successor.right:
            current = successor
            successor = successor.parent
        return successor

    def predecessor(self,current):
        if current.left:
            return self.maximum(current.left)
        pre = current.parent
        while pre and current == pre.left:
            current = pre
            pre = pre.parent
        return pre

    def inorder_walk(self):
        inorderarr = []
        root = self.minimum()
        while root:
            inorderarr.append(root)
            root = self.successor(root)
        return inorderarr

    def nodecounter(self):
        checklist = self.inorder_walk()
        count = 0
        for i in checklist:
            if i.color == Node.Black:
                count = count + 1
        return count

    def search(self, key):
        FoundNode = self.root
        while FoundNode and FoundNode.key != key:
            if key < FoundNode.key:
                FoundNode = FoundNode.left
            else:
                FoundNode = FoundNode.right
        return FoundNode

    def nearsearch(self,key):
        node = self.root
        nearnode = self.root
        diff = self.maximum().key
        while node and nearnode.key != key:
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


    def is_empty(self):
        return bool(self.root)

    def blackheight(self):
        root = self.root
        height = 0
        while root:
            root = root.left
            if not root or root.color == Node.Black:
                height += 1
        return height

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left: y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right: y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.right = x
        x.parent = y



    def delete_fixup(self, x):
        while x != self.root and x.color == Node.Black:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == Node.Red:
                    w.color = Node.Black
                    x.parent.color = Node.Red
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == Node.Black and w.right.color == Node.Black:
                    w.color = Node.Red
                    x = x.parent
                else:
                    if w.right.color == Node.Black:
                        w.left.color = Node.Black
                        w.color = Node.Red
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = Node.Black
                    w.right.color = Node.Black
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == Node.Red:
                    w.color = Node.Black
                    x.parent.color = Node.Red
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == Node.Black and w.left.color == Node.Black:
                    w.color = Node.Red
                    x = x.parent
                else:
                    if w.left.color == Node.Black:
                        w.right.color = Node.Black
                        w.color = Node.Red
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = Node.Black
                    w.left.color = Node.Black
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = Node.Black


def main():
    f = open("input.txt", 'r')
    tmpdata = f.read()
    data = tmpdata.split()
    f.close()
    tree = RedBlackTree()

    g = open("search.txt",'r')
    tmpdata2 = g.read()
    data2 = tmpdata2.split()
    g.close()

    w = open("output.txt",'w')

    for i in data:
        if int(i) > 0:
            tree.insert(Node(int(i)))
        elif int(i) <0:
            findnode = tree.search(abs(int(i)))
            tree.delete(findnode)
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
