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

#lengthoflongestSubstring
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        result = 0
        substringlen = 1
        while substringlen <= len(s):
            found = False
            for i in range(len(s) - substringlen + 1): #how often we can loop through (can be optimized further)
                substring = s[i:substringlen+i] #each substring possible
                if len(substring) == len(set(substring)): #check if there are no duplicates
                    found = True #dont leave yet check larger substrings
                    result = substringlen #this is the highest we found
                    break #we need to check a larger length since we found out we have a substring with no dupes
            if found == False:
                break
            substringlen += 1
        return result

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        merged = sorted(nums1 + nums2)
        if (len(merged)%2==0):
            return((merged[len(merged)//2]+merged[len(merged)//2-1])/2)
        else:
            return(merged[len(merged)//2])

#longest palindrome substring
class Solution:
    def longestPalindrome(self, s: str) -> str:
        found = False #s == s[::-1]
        pal = s[0]
        pallen = 1
        while pallen <= len(s):
            found = False
            for i in range(len(s) - pallen + 1): #loops the number of times we have substrings of this length
                subs = s[i:pallen+1]
                if subs == subs[::-1]: #check if its a palindrome
                    found = True #we can keep going
                    pal = subs
                    break #we can skip to the next size since we found a pal
            if found == False:
                break #we havent found a palindrome at this length
            pallen += 1 #we can go to the next size up
        return pal