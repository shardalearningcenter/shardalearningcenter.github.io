---
layout: post
title: "Lottery Analogy for Reservoir Sampling algorithm leetcode problem facebook"
date: 2025-09-18
---


# Lottery Analogy for Reservoir Sampling (k = 1)

Imagine you are running a lucky draw at a fair.

People come in one by one.

You must always keep exactly one name in your box.

You don’t know how many people will come.

# Step by step:

## First person (A) comes → you put A in the box (no choice, it’s empty).

Box: [A]

## Second person (B) comes →
You flip a fair coin:

Heads → replace A with B.

Tails → keep A.

Now, <mark>A and B both have equal chance (50%).</mark>

### Third person (C) comes →
You roll a 3-sided dice (imagine).

If it lands on side 1 → replace box with C.

Otherwise (2 or 3) → keep the old one (A or B).

👉 Now A, B, C each have equal chance (1/3).

### Fourth person (D) comes →
Roll a 4-sided dice.

If side 1 → replace with D.

Otherwise keep old one.

👉 Each of A, B, C, D has equal chance (1/4).