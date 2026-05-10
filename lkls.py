class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class LinkedList():
    def __init__(self):
        self.first = None
        self.current = None
        self.last = None
        self.size = 0
        self.index = None

    def append(self, element):
        node = Node(element)
        if self.size == 0:
            self.first = node
            self.last = node
            self.current = node
            self.index = 0
        else:
            node.prev = self.last
            self.last.next = node
            self.last = node
            self.current = self.last
            self.index = self.size
        self.size += 1
    
    def len(self):
        return self.size

    def insert(self, element, index):
        if index < 0 or index > self.size:
            raise IndexError("OutOfRange")
        
        if index == 0:
            if self.size == 0:
                self.append(element)
            else:
                node = Node(element)
                node.next = self.first
                self.first.prev = node
                self.first = node
                self.size += 1
        elif index == self.size:
            self.append(element)
        else:
            self.set_cursor(index)
            node = Node(element)
            #prev = [prev, data, next = replace]
            self.current.prev.next = node
            #node = [prev = replace, data, next]
            node.prev = self.current.prev
            #node = [prev, data, nxt = replace]
            node.next = self.current
            #next = [rev = replace, data, next]
            self.current.prev = node
            self.current = node
            self.size += 1
    
    def set_cursor(self, index):
        if index < 0 or index > self.size:
            raise IndexError("OutOfRange")
        
        if index == 0:
            self.current = self.first
            self.index = 0
            
        elif index == self.size - 1:
            self.current = self.last
            self.index = self.size-1
        elif index == self.index:
            pass
        else:
            if abs(index-self.index) > index:
                self.current = self.first
                self.index = 0
                for i in range(index):
                    self.step_up()
            elif self.size-index < index:
                self.current = self.last
                self.index = self.size - 1
                for i in range(self.size-index):
                    self.step_down()
            elif self.index > index:
                for i in range(self.index - index):
                    self.step_down()
            else:
                for i in range(index-self.index):
                    self.step_up()

    def get(self):
        return self.current.data

    def find(self, index):
        self.set_cursor(index)
        return self.get()

    def delete(self, index):
        if index < 0 or index > self.size:
            raise IndexError("OutOfRange")
        
        if index == 0:
            if self.size == 1:
                self.first = None
                self.last = None
                self.current = None
                self.index = None
            else:
                self.first = self.first.next
                if self.index == 0:
                    self.current = self.first
        elif index == self.size - 1:
            self.last = self.last.prev
            self.last.next = None
            if self.index == self.size - 2:
                self.current = self.last
                self.index = self.size - 2
        else:
            self.set_cursor(index)
            self.current.prev.next = self.current.next
            self.current = self.current.next
        self.size -= 1

        
    def step_up(self):
        if self.index < self.size - 1:
            self.current = self.current.next
            self.index += 1

    def step_down(self):
        if self.index > 0:
            self.current = self.current.prev
            self.index -= 1

    def __str__(self):
        element = []
        temp = self.first
        for i in range(self.size):
            element.append(str(temp.data))
            temp = temp.next
        return " <-> ".join(element)

if __name__ == "__main__":
    test = LinkedList()
    for i in range(10):
        test.append(i)
    print(test.find(9))