---
layout: post
title: "DP patterns Matrix Multiplication"
date: 2025-08-24
tags: [LeetCode, Dynamic Programming, Algorithms, Interview Prep]
---
# 312. Burst Balloons

You are given n balloons, indexed from 0 to n - 1. Each balloon is painted with a number on it represented by an array nums. You are asked to burst all the balloons.

If you burst the <mark>ith balloon</mark>, you will get <mark>nums[i - 1] * nums[i] * nums[i + 1] coins<mark>. If i - 1 or i + 1 goes out of bounds of the array, then treat it as if there is a balloon with a 1 painted on it.

Return the <mark>maximum coins</mark> you can collect by bursting the balloons wisely.

 

- Example 1:

Input: nums = [3,1,5,8]
Output: 167
Explanation:
nums = [3,1,5,8] --> [3,5,8] --> [3,8] --> [8] --> []
coins =  3*1*5    +   3*5*8   +  1*3*8  + 1*8*1 = 167
- Example 2:

Input: nums = [1,5]
Output: 10

# intution
<details open>
<mark>
Think reverse: last balloon to burst
Instead of asking which to burst first, ask which balloon will be the last to burst in a subarray.
</mark>

<mark>
If i is the last balloon in some range (left, right), then bursting it gives nums[left] * nums[i] * nums[right].
</mark>

All balloons between left and i and between i and right must already be burst optimally.
</mark>

```java
for (int i = left; i <= right; i++) {
            // nums[i] is the last burst one
            int gain = nums[left - 1] * nums[i] * nums[right + 1];
            int leftP=dp(memo, nums, left, i - 1);
           
            int rightP=dp(memo, nums, i + 1, right);
            //System.out.println("rightP "+rightP);

            // nums[i] is fixed, recursively call left side and right side
            int remaining =  leftP+ rightP;
            result = Math.max(result, remaining + gain);
        }
```
</details>


```java

class Solution {
    public int maxCoins(int[] nums) {
        int a=1000000000;
        // add 1 before and after nums
        int n = nums.length + 2;
        int[] newNums = new int[n];
        System.arraycopy(nums, 0, newNums, 1, n - 2);
        newNums[0] = 1;
        newNums[n - 1] = 1;

        // cache the results of dp
        int[][] memo = new int[n][n];

        // we can not burst the first one and the last one
        // since they are both fake balloons added by ourselves
        return dp(memo, newNums, 1, n - 2);
    }

    public int dp(int[][] memo, int[] nums, int left, int right) {
        // return maximum if we burst all nums[left]...nums[right], inclusive
        if (right - left < 0) {
            return 0;
        }

        // we've already seen this, return from cache
        if (memo[left][right] > 0) {
            return memo[left][right];
        }

        // find the last burst one in nums[left]...nums[right]
        int result = 0;
        for (int i = left; i <= right; i++) {
            // nums[i] is the last burst one
            int gain = nums[left - 1] * nums[i] * nums[right + 1];
            int leftP=dp(memo, nums, left, i - 1);
           // System.out.println("i "+1);
         //   System.out.println("leftP "+leftP);
            int rightP=dp(memo, nums, i + 1, right);
            //System.out.println("rightP "+rightP);

            // nums[i] is fixed, recursively call left side and right side
            int remaining =  leftP+ rightP;
            result = Math.max(result, remaining + gain);
        }
        // add to the cache
        memo[left][right] = result;
        return result;
    }
}

```
