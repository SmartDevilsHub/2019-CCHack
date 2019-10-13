class Queue:
    def __init__(self, lst=[]):
        self.storage = list(lst)

    def __len__(self):
        return len(self.storage)

    def print(self):
        print(self.storage)

    def push(self, item):
        self.storage.append(item)

    def pop(self):
        return self.storage.pop(0)

    def peek(self):
        return self.storage[0]

    def clear(self):
        self.storage = list()
