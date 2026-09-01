#a collection of my answers for leetcode questions, for practice and reference

#first question
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            target2 = target - num #this is the second number needed
            if target2 in seen:
                return [seen[target2], i] #returns the index of the pre processed number and the current one together
            seen[num] = i #stores the index of the number + the number itself once processed

#second question 2 solutions the second one is the first solution i came up with, the first one is a more efficient solution but its harder to read
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        carry = 0
        l3 = ListNode()
        current = l3
        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            temp = val1 + val2 + carry
            carry = 0

            carry = temp // 10
            temp = temp % 10

            current.next = ListNode(temp)
            current = current.next
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next
            print(current)
        return(l3.next)

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        carry = 0
        l3 = ListNode()
        current = l3
        while l1 or l2 or carry > 0:
            if l1 == None:
                l1 = ListNode(0)
            if l2 == None:
                l2 = ListNode(0)
            temp = l1.val + l2.val + carry
            carry = 0
            if temp > 9:
                carry = temp // 10
                temp = temp % 10
            current.next = ListNode(temp)
            current = current.next
            l1 = l1.next
            l2 = l2.next
            print(current)
        return(l3.next)