class LinkedNode:
    def __init__(self, key = None, next=None): 
        self.key = key
        self.next = next

    def __str__(self):
        return str({
            'key': self.key,
            'next.key': self.next.key if self.next != None else None
        })

    @staticmethod
    def to_linked_list(arr):
        head = LinkedNode()
        node = head
        for i in range(len(arr)):
            node.key = arr[i]
            if i < len(arr) - 1 :
                node.next = LinkedNode()
            node = node.next
        return head
    @staticmethod
    def to_list(head):
        max = 20
        node = head
        result = []
        count = 0
        while node != None:
            if count > max: break
            result.append(node.key)
            node = node.next
            count += 1
        return result