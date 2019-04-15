#!/usr/bin/python3


class ListNode:
    def __init__(self, x=None):
        self.val = x
        self.next = None

    def __repr__(self):
        tmp = self
        s = []
        while tmp:
            s.append(tmp.val)
            tmp = tmp.next
        return '->'.join([str(i) for i in s])

    def append(self, x):
        while self.next:
            self = self.next
        self.next = ListNode(x)

    def extend(self, x):
        for i in x:
            self.append(i)

    @staticmethod
    def merge(l1, l2):
        merged = ListNode(0)
        head = merged
        while l1 and l2:
            print(head)
            merged.next = ListNode(l1.val)
            merged = merged.next
            merged.next = ListNode(l2.val)
            merged = merged.next
            l1 = l1.next
            l2 = l2.next
        return head.next


l1 = ListNode(1)
for i in (2, 3):
    l1.append(i)
print(f'l1 {l1}')
l2 = ListNode(4)
l2.extend([5, 6])
print('l2', l2)
print('merge', ListNode.merge(l1, l2))
