# Implementation of Hash Table, Singly Linked List, Doubly Linked List and Binary Search Tree 

# =============================================================================

class SinglyLinkedNode(object):
    def __init__(self, item=None, next_link=None):
        super(SinglyLinkedNode, self).__init__()
        self._item = item
        self._next = next_link

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        return repr(self.item)


class SinglyLinkedList(object):
    def __init__(self):
        super(SinglyLinkedList, self).__init__()
        self.size = 0
        self.head = None
        self.tail = None

    def __len__(self):
        return self.size

    def __iter__(self):
        nptr = self.head
        while nptr is not None:
            yield nptr.item
            nptr = nptr.next

    def __contains__(self, item):
        nptr = self.head
        while nptr is not None:
            if (nptr.item == item):
                break
            else:
                # trlr = nptr
                nptr = nptr.next
        if (nptr is None):
            return False
        else:
            return True

    def remove(self, item):
        nptr = self.head
        trlr = self.head

        if (self.__contains__(item)):
            if (self.size == 1):
                self.head = None
                self.tail = None
                self.size -= 1
            elif (self.head.item == item):
                self.head = self.head.next
                self.size -= 1
            else:
                while nptr.item != item:
                    trlr = nptr
                    nptr = nptr.next
                if (self.tail.item == nptr.item):
                    self.tail = trlr
                    self.tail.next = None
                    self.size -= 1
                else:
                    trlr.next = nptr.next
                    self.size -= 1
            return True
        else:
            return False

    def prepend(self, item):
        node = SinglyLinkedNode(item)
        if (self.head is None):
            self.head = node
            self.tail = node
            self.size = self.size + 1
        else:
            node._next = self.head
            self.head = node
            self.size += 1
        return True

    def __repr__(self):
        s = "List:" + "->".join([str(item) for item in self])
        return s


# =============================================================================

class BinaryTreeNode(object):
    def __init__(self, data=None, left=None, right=None, parent=None):
        super(BinaryTreeNode, self).__init__()
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent


class BinarySearchTreeDict(object):
    def __init__(self):
        super(BinarySearchTreeDict, self).__init__()
        self.size = 0
        self.root = BinaryTreeNode()
        self.node_dict = {}
        # self.node_dict = [[]]

    @property
    def length(self):
        return self.size

    def get_h(self):
        if self.root is None:
            return -1
        else:
            leftheight = self.leftSubtree().get_h()

            rightheight = self.rightSubtree().get_h()

            return max(leftheight, rightheight) + 1

    @property
    def height(self):
        if self.size == 0:
            return -1
        else:
            return self.get_h()

    def __repr__(self):
        s = "Inorder:" + "->".join([str(item) for item in self.inorder_keys()])
        p = "Preorder:" + "->".join([str(item) for item
                                     in self.preorder_keys()])
        return [s, p]

    def leftSubtree(self):
        leftTree = BinarySearchTreeDict()
        leftTree.root = self.root.left
        return leftTree

    def rightSubtree(self):
        rightTree = BinarySearchTreeDict()
        rightTree.root = self.root.right
        return rightTree

    def inorder_keyvalue(self):
        if (self.root is None):
            raise StopIteration
        else:
            for i in self.leftSubtree().inorder_keyvalue():
                yield i

            yield self.root.data

            for j in self.rightSubtree().inorder_keyvalue():
                yield j

    def inorder_keys(self):
        # Using the 'yield'  keyword and StopIteration exception
        if (self.root is None):
            raise StopIteration
        else:
            for i in self.leftSubtree().inorder_keys():
                yield i

            yield self.root.data[0]

            for j in self.rightSubtree().inorder_keys():
                yield j

    def postorder_keys(self):
        # Using 'yield' and 'StopIteration' to yield key in POSTORDER
        if (self.root is None):
            raise StopIteration
        else:
            for k in self.leftSubtree().postorder_keys():
                yield k

            for l in self.rightSubtree().postorder_keys():
                yield l

            yield self.root.data[0]

    def preorder_keys(self):
        # Using 'yield' and 'StopIteration' to yield key in PREORDER
        if (self.root is None):
            raise StopIteration
        else:

            yield self.root.data[0]

            for m in self.leftSubtree().preorder_keys():
                yield m

            for n in self.rightSubtree().preorder_keys():
                yield n

    def _items(self):
        # Using 'yield' to return the items (key and value) using
        # an INORDER traversal.

        for a in self.inorder_keyvalue():
            yield a
        print

    def __getitem__(self, key):
        # Using Get the VALUE associated with key
        nptr = self.root

        while (nptr is not None):

            if (nptr.data[0] == key):
                break
            if (nptr.data[0] <= key):
                nptr = nptr.left
            else:
                nptr = nptr.right
        if (nptr is None):
            return None
        else:
            return nptr.data[1]

    def __setitem__(self, key, value):
        if (key is None):
            return False
        else:
            if (self.size != 0 and self.__contains__(key)):
                # current_value = self.__getitem__(key)
                # self.node_dict[key] = value
                nptr = self.root

                while not (nptr is None):
                    if (key == nptr.data[0]):
                        break
                    if (key <= nptr.data[0]):
                        nptr = nptr.left
                    else:
                        nptr = nptr.right
                nptr.data[1] = value
                self.node_dict[key] = value
                # self.node_dict.
            else:
                new = BinaryTreeNode([key, value])

                if (self.size == 0):
                    self.root = new
                    self.size += 1
                    self.node_dict[key] = value

                else:
                    temp = self.root
                    ptr = temp
                    while not (temp is None):
                        if (key <= temp.data[0]):
                            ptr = temp
                            temp = temp.left
                        else:
                            ptr = temp
                            temp = temp.right
                    if (key <= ptr.data[0]):
                        ptr.left = new
                        new.parent = ptr
                        self.size += 1
                        self.node_dict[key] = value
                    else:
                        ptr.right = new
                        new.parent = ptr
                        self.size += 1
                        self.node_dict[key] = value
            return True

    def successor(self, x):
        temp = x.right
        while (temp.left is not None):
            temp = temp.left
        return temp

    def __delitem__(self, key):

        delete_node = self.root

        if (self.__contains__(key)):

            while (key != delete_node.data[0]):
                if (key <= delete_node.data[0]):
                    delete_node = delete_node.left
                else:
                    delete_node = delete_node.right
            # condition 1 delete node has no child
            if (delete_node.left is None and delete_node.right is None):
                if (delete_node.parent.left == delete_node):
                    # remove directory entry
                    self.node_dict.pop(key)
                    self.size -= 1
                    # remove tree link
                    delete_node.parent.left = None

                else:
                    # delete directory entry
                    self.node_dict.pop(key)
                    self.size -= 1
                    # remove tree link
                    delete_node.parent.right = None
            # case 2 delete node has only left child
            elif (delete_node.left is not None and delete_node.right is None
                  and delete_node.left.left is None
                  and delete_node.left.right is None):
                delete_node.data = delete_node.left.key
                self.node_dict.pop(key)
                self.size -= 1
                delete_node.left = None
            # Delete node has only right child
            elif (delete_node.left is None and delete_node.right is not None
                  and delete_node.right.left is None
                  and delete_node.right.right is None):

                delete_node.data = delete_node.right.data
                self.node_dict.pop(key)
                self.size -= 1
                delete_node.right = None
            # delete node has 2 childs
            else:
                successor = self.successor(delete_node)
                # x = delete_node

                delete_node.data = successor.data
                #             case 1 succeessor has no child
                if (successor.left is None and successor.right is None):
                    if (successor.parent.left == successor):
                        self.node_dict.pop(key)
                        self.size -= 1
                        successor.parent.left = None
                    else:
                        self.node_dict.pop(key)
                        self.size -= 1
                        successor.parent.right = None
                elif (successor.left is not None
                      and successor.right is None):
                    successor.data = successor.left.data
                    successor.right = successor.left.right
                    self.node_dict.pop(key)
                    self.size -= 1
                    successor.left = None
                elif (successor.left is None
                      and successor.right is not None):

                    successor.data = successor.right.data
                    successor.left = successor.right.left
                    self.node_dict.pop(key)
                    self.size -= 1
                    successor.right = None
            return True
        else:
            return False

    def __contains__(self, key):
        
        nptr = self.root

        if self.size == 0:
            return False

        else:

            while not (nptr is None):

                if (nptr.data[0] == key):
                    break

                if (key <= nptr.data[0]):
                    nptr = nptr.left
                else:
                    nptr = nptr.right

            if (nptr is None):
                return False
            else:
                return True

    def __len__(self):
        return self.size

    def display(self):

        return self.__repr__()


# =============================================================================
class DoublyLinkedNode(object):
    def __init__(self, key=None, value=None, next=None, prev=None):
        super(DoublyLinkedNode, self).__init__()
        self.key = key
        self.value = value
        self.next = next
        self.prev = prev


class ChainedHashDict(object):
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(ChainedHashDict, self).__init__()

        self._bin_count = bin_count
        self.max_load = max_load
        self._hashfunc = hashfunc
        self.list = [DoublyLinkedNode() for i in range(bin_count)]
        self.size = 0

        # Construct a new table

    @property
    def load_factor(self):
        lf = (float(self.size) / float(self._bin_count))
        return lf

    @property
    def len(self):
        return self.size

    @property
    def bin_count(self):
        # if self.size == None:
        return self._bin_count

    def rebuild(self, newSize):
        # Rebuild this hash table with a new bin count
        new_list = self.list
        # new_length = bincount * 2
        self.list = [DoublyLinkedNode() for i in range(newSize)]
        self._bin_count = newSize
        self.size = 0
        for j in range(len(new_list)):
            if new_list[j].key is not None:
                # self.__setitem__(new_list[j].key, new_list[j].key)
                nptr = new_list[j]
                while nptr is not None:
                    self.__setitem__(nptr.key, nptr.value)
                    nptr = nptr.next

    def __getitem__(self, key):
        # Using Get the VALUE associated with key
        if key is not None:
            i = self._hashfunc(key) % self._bin_count
            if self.list[i].key is None:
                return None
            else:

                nptr = self.list[i]
                while nptr.next is not None:
                    if nptr.key == key:
                        break
                    nptr = nptr.next
                if nptr.key == key:
                    return nptr.value
                else:
                    return None
        else:
            return None

    def __setitem__(self, key, value):
        
        existingValue = self.__getitem__(key)
        if existingValue is not None:
            i = self._hashfunc(key) % self._bin_count
            nptr = self.list[i]
            while nptr.key != key:
                nptr = nptr.next
            nptr.value = value
        else:
            if (self.load_factor > self.max_load):
                self.rebuild(self.bin_count * 2)
            if key is not None:
                i = self._hashfunc(key) % self._bin_count
                if not (self.list[i].key is None):
                    new = DoublyLinkedNode(key, value)

                    new.next = self.list[i]
                    self.list[i].prev = new
                    self.list[i] = new
                    new.prev = new
                else:
                    new = DoublyLinkedNode(key, value)
                    new.prev = new
                    self.list[i] = new
                self.size += 1
                return True
            else:
                return False

    def __delitem__(self, key):
       
        if not (key is None):
            if self.__contains__(key):
                i = self._hashfunc(key) % self._bin_count
                nptr = self.list[i]
                while nptr.key != key:
                    nptr = nptr.next
                if nptr == self.list[i] and nptr.next is None:
                    self.list[i] = None
                elif nptr == self.list[i]:
                    self.list[i] = self.list[i].next
                    self.list[i].prev = self.list[i]
                elif nptr.next is None:
                    nptr.prev.next = None
                    self.list[i].prev = nptr.prev
                else:
                    nptr.prev.next = nptr.next
                self.size -= 1
                return True
            else:
                return False
        else:
            return False

    def __contains__(self, key):

        if key is not None:
            i = self._hashfunc(key) % self._bin_count

            if self.list[i] is None:
                return False
            else:
                nptr = self.list[i]
                while nptr.next is not None:
                    if nptr.key == key:
                        break
                    nptr = nptr.next
                if nptr.key == key:
                    return True
                else:
                    return False

    def __len__(self):
        return self.size

    def __iter__(self, p):
        nptr = self.list[p]
        while nptr:
            yield [nptr.key, nptr.value]
            nptr = nptr.next

    def __repr__(self):
        count = 0

        for i in self.list:

            yield count
            yield "list:"

            if i.key:
                if i.next:
                    j = i
                    # while j:
                    p = self._hashfunc(j.key) % self._bin_count
                    yield "->".join(str(r) for r in self.__iter__(p))
                else:
                    yield [i.key, i.value]
                    #
                count = count + 1
            else:
                count = count + 1
            yield "\n"

    def display(self):
        # Return a string showing the table with multiple lines
        
        ans = "".join([str(i) for i in self.__repr__()])
        return ans


class OpenAddressHashDict(object):
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(OpenAddressHashDict, self).__init__()
        self._bin_count = bin_count
        self.max_load = max_load
        self._hashfunc = hashfunc
        self.list = [[] for i in range(bin_count)]
        # self.list = [[None,None] for i in range(bin_count)]
        self.size = 0

    @property
    def load_factor(self):
        lf = (float(self.size) / float(self._bin_count))
        return lf

    @property
    def len(self):
        return self.size

    @property
    def bin_count(self):
        # if self.size == None:
        return self._bin_count

    def rebuild(self, bincount):
        new_list = self.list
        # new_length = bincount * 2
        self.list = [[] for i in range(bincount)]
        self._bin_count = bincount
        self.size = 0
        for j in range(len(new_list)):
            if new_list[j]:
                self.__setitem__(new_list[j][0], new_list[j][1])

    def __getitem__(self, key):

        if key is not None:
            i = self._hashfunc(key) % self._bin_count
            if self.list and self.list[i]:
                while self.list[i]:
                    if self.list[i][0] == key:
                        break
                    i = i + 1
                if not self.list[i]:

                    return None
                else:
                    return self.list[i][1]
            else:
                return None
        else:
            return None

    def __setitem__(self, key, value):
        existingValue = self.__getitem__(key)
        if existingValue is not None:
            i = self._hashfunc(key) % self._bin_count
            # nptr = self.list[i]
            while self.list[i][0] != key:
                i = (i + 1) % self._bin_count
            self.list[i][1] = value
        else:
            if (self.load_factor >= self.max_load):
                self.rebuild(self.bin_count * 2)
            if key is not None:
                i = self._hashfunc(key) % self._bin_count
                if not self.list[i]:
                    self.list[i] = [key, value]
                else:
                    while self.list[i]:
                        if self.list[i][0] == -1:
                            break
                        i = i + 1
                    self.list[i] = [key, value]
                self.size += 1
                return True
            else:
                return False

    def __delitem__(self, key):

        if not (key is None):
            if self.__contains__(key):
                i = self._hashfunc(key) % self._bin_count

                while self.list[i][0] != key:
                    i = i + 1
                # self.list[i] = []
                self.list[i] = [-1, "Deleted"]

                self.size -= 1
                return True
            else:
                return False
        else:
            return False

    def __contains__(self, key):

        if key is not None:
            i = self._hashfunc(key) % self._bin_count
            if self.list and self.list[i]:
                while self.list[i]:
                    if self.list[i][0] == key:
                        break
                    i = i + 1
                if not self.list[i]:

                    return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def __len__(self):
        return self.size

    def __repr__(self):
        count = 0

        for i in self.list:

            yield "bin "
            yield count
            yield ": "
            if i:
                yield [self.list[count][0], str(self.list[count][1])]
            else:
                yield [None, None]

            count = count + 1
            yield "\n"

    def display(self):
        # Return a string showing the table with multiple lines
        
        ans = "".join([str(i) for i in self.__repr__()])
        return ans


def terrible_hash(bin):
    """A terrible hash function that can be used for testing.

    A hash function should produce unpredictable results,
    but it is useful to see what happens to a hash table when
    you use the worst-possible hash function.  The function
    returned from this factory function will always return
    the same number, regardless of the key.

    :param bin:
        The result of the hash function, regardless of which
        item is used.

    :return:
        A python function that can be passed into the constructor
        of a hash table to use for hashing objects.
    """

    def hashfunc(item):
        return bin

    return hashfunc


def main():
    pass

if __name__ == '__main__':
    main()
