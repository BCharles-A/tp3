class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class LinkedList():
    def __init__(self, element):

        node = Node(element)

        self.first = node
        self.current = node
        self.last = node

    def append(self, element):
        node = Node(element)
        if self.last is None:
            self.last = node
            self.first = node
            self.current = node
        else:
            self.last.next = node
            node.prev = self.last
            self.last = node
    def len(self):
        element = []
        temp = self.first
        while temp:
            element.append(str(temp.data))
            temp = temp.next
        return len(element)

    #def ajout_indice(self, element, index):  #PAS FINI
        node = Node(element)
        if index >= self.len()+1:
            self.append(element)
        else:
            self.current = self.first
            for i in range(index-1):
                self.show_next()
            node.prev = self.current.prev
            node.next = self.current.next
            self.current.prev = node
            self.current = node
        return self  
    
    def show_next(self):
        if(self.current.next != None):
            self.current = self.current.next
        return self.current

    def show_prev(self):
        if(self.current.prev != None):
            self.current = self.current.prev
        return self.current

    def afficher(self):
        element = []
        temp = self.first
        while temp:
            element.append(str(temp.data))
            temp = temp.next
        print(" <-> ".join(element))



l = LinkedList(3)
l.append(2)
l.append(4)
l.append(5)
l.append(4)
l.append(3)
l.ajout_indice(10, 3)
l.afficher()
