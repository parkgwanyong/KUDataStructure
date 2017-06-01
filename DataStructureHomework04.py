

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

    def insert(self, x):
        self.insert_fixup(x)

        x.color = Node.Red
        while x != self.root and x.parent.color == Node.Red:
            if x.parent == x.parent.parent.left:
                y = x.parent.parent.right
                if y and y.color == Node.Red:
                    x.parent.color = Node.Black
                    y.color = Node.Black
                    x.parent.parent.color = Node.Red
                    x = x.parent.parent
                else:
                    if x == x.parent.right:
                        x = x.parent
                        self.left_rotate(x)
                    x.parent.color = Node.Black
                    x.parent.parent.color = Node.Red
                    self.right_rotate(x.parent.parent)
            else:
                y = x.parent.parent.left
                if y and y.color == Node.Red:
                    x.parent.color = Node.Black
                    y.color = Node.Black
                    x.parent.parent.color = Node.Red
                    x = x.parent.parent
                else:
                    if x == x.parent.left:
                        x = x.parent
                        self.right_rotate(x)
                    x.parent.color = Node.Black
                    x.parent.parent.color = Node.Red
                    self.left_rotate(x.parent.parent)
        self.root.color = Node.Black


    def insert_fixup(self, z):
        y = NilNode.instance()
        x = self.root
        while x:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if not y:
            self.root = z
        else:
            if z.key < y.key:
                y.left = z
            else:
                y.right = z

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

    def minimum(self, x=None):
        if x is None: x = self.root
        while x.left:
            x = x.left
        return x

    def maximum(self, x=None):
        if x is None: x = self.root
        while x.right:
            x = x.right
        return x

    def successor(self, x):
        if x.right:
            return self.minimum(x.right)
        y = x.parent
        while y and x == y.right:
            x = y
            y = y.parent
        return y


    def inorder_walk(self, x=None):
        inorderarr = []
        if x is None: x = self.root
        x = self.minimum()
        while x:
            inorderarr.append(x)
            x = self.successor(x)
        return inorderarr

    def nodecounter(self):
        checklist = self.inorder_walk()
        count = 0
        for i in checklist:
            if i.color == Node.Black:
                count = count + 1
        return count

    def search(self, key, x=None):
        if x is None: x = self.root
        while x and x.key != key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def is_empty(self):
        return bool(self.root)

    def blackheight(self, x=None):
        if x is None: x = self.root
        height = 0
        while x:
            x = x.left
            if not x or x.color ==Node.Black:
                height += 1
        return height

    def left_rotate(self, x):
        if not x.right:
            raise "x.right is nil!"
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
        if not x.left:
            raise "x.left is nil!"
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
    for i in data:
        if int(i) > 0:
            tree.insert(Node(int(i)))
        elif int(i) <0:
            findnode = tree.search(abs(int(i)))
            tree.delete(findnode)
        else:
            inorder = tree.inorder_walk()
            print("total = {0}".format(len(inorder)))
            print("nb = {0}".format(tree.nodecounter()))
            print("blackheight = {0}".format(tree.blackheight()))
            for key in inorder:
                print(key.key)

main()
