class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

head = ListNode(2)
head.next = ListNode(4)
head.next.next = ListNode(3)

head2 = ListNode(5)
head2.next = ListNode(6)
head2.next.next = ListNode(4)

strl1 = ""
strl2 = ""

lengthl1 = 0
lengthl2 = 0

l1 = head
l2 = head2
while l1 is not None:
    lengthl1 += 1
    strl1 += str(l1.val)
    l1 = l1.next
while l2 is not None:
    lengthl2 += 1
    strl2 += str(l2.val)
    l2 = l2.next
    
strl1 = strl1[::-1]
strl2 = strl2[::-1]

resultList = [int(i) for i in str(int(strl1) + int(strl2))]
resultList.reverse()

resultNode = None
for i in resultList:
    resultNode = ListNode(i, resultNode)    
    
prev = None
current = resultNode
while current is not None:
    next = current.next
    current.next = prev
    prev = current
    current = next
resultNode = prev

print(resultNode.val, resultNode.next.val, resultNode.next.next.val)
