class Queue:
    def __init__(self, size = 20):
        self.size = size
        self.items = [None]*size
        self.end = 0
        self.start = 0

    def enqueue(self, item):
        # return false if space is filled
        if self.items[self.end] != None: return False
        # add item
        self.items[self.end] = item
        # increment end pointer
        self.end +=1
        # move end pointer to beginning if outside range
        if self.end >= self.size: self.end = 0
        # return true on success
        return True

    def dequeue(self):
        # store item to be popped
        item = self.items[self.start]
        # return None if empty
        if item == None: return None
        # remove item
        self.items[self.start] = None
        # increment start
        self.start += 1
        # move start pointer to beginning if outside range
        if self.start >= self.size: self.start = 0
        return item
    
    def is_empty(self):
        return self.start == self.end
    
    def __str__(self):
        return str({
            'start': self.start,
            'end': self.end,
            'items': self.items
        })

class Stack:
    def __init__(self, size):
        self.size = size
        self.items = [None]*size
        self.pointer = -1

    def push(self, item):
        
        # return False if no space left in array
        if self.pointer+1 >= self.size: return False

        # increment pointer
        self.pointer += 1

        # set array value
        self.items[self.pointer] = item

       # return True on success
        return True

    def pop(self):
        item = self.items[self.pointer] 
        self.items[self.pointer] = None
        self.pointer = max(-1, self.pointer-1)
        return item

    def change(self, item):
        self.items[self.pointer] = item

    def peek(self):
        item = self.items[self.pointer]
        return item

    def empty(self):
        return self.items[self.pointer] == None
    
    def __str__(self):
        return str({
            'pointer': self.pointer,
            'items': self.items
        })