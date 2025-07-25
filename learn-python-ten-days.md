---
layout: page
title: Python 10 Days Bootcamp
permalink: /learn-python-ten-days/
---
# 🐍 Learn Python in 10 Days – Hands-On Roadmap

> Learn Python by building small, real projects every day. No fluff. No long lectures. Just code and confidence.

---
# Python Sample exercize 

## [Link to list of python beginner level exercize](https://shardalearningcenter.github.io/2025/07/25/python-beginner-exercize.html)

## 📅 Day 1: Hello Python & Setup

### 🔍 What You'll Learn
- Install Python
- Run your first `.py` file
- Print text and numbers
- Variables and data types

### 🛠️ Let's Do It
```python
print("Hello, Python!")
name = input("What’s your name? ")
age = int(input("How old are you? "))
print(f"{name}, you’ll be {age+1} next year!")
```

### 🎯 Task
- Create a file named `hello.py`
- Ask the user’s name and age
- Greet them with a message using `f-string`

---

## 📅 Day 2: Conditions & Loops

### 🔍 What You'll Learn
- `if`, `elif`, `else`
- `for`, `while` loops
- `break` and `continue`

### 🛠️ Let's Do It
```python
num = int(input("Guess a number: "))
if num == 7:
    print("Correct!")
else:
    print("Try again!")
```

```python
# Count 1 to 5 using loop
for i in range(1, 6):
    print(i)
```

### 🎯 Task
- Build a number guessing game (max 3 tries)
- Add a secret number with a hint

---

## 📅 Day 3: Functions & Reuse

### 🔍 What You'll Learn
- `def`, parameters, return
- Reusable code blocks

### 🛠️ Let's Do It
```python
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
```

### 🎯 Task
- Write a function that adds 2 numbers
- Write a function that checks if a number is even

---

## 📅 Day 4: Strings & Input Formatting

### 🔍 What You'll Learn
- String methods: `.lower()`, `.upper()`, `.replace()`
- Slicing and indexing

### 🛠️ Let's Do It
```python
msg = "Learn Python"
print(msg.upper())
print(msg[0:5])  # 'Learn'
```

### 🎯 Task
- Create a sentence reverser
- Input: "Python is fun" → Output: "fun is Python"

---

## 📅 Day 5: Lists & Loops

### 🔍 What You'll Learn
- Creating and accessing lists
- `append()`, `pop()`, slicing

### 🛠️ Let's Do It
### Add
```python
fruits = ["apple", "banana", "cherry"]
fruits.append("kiwi")
print(fruits)
```
### Remove 
```python
fruits = ["apple", "banana", "cherry"]
fruits.remove("apple")
print(fruits)
```
### Loop list
```python

fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
  print(fruit)

```

### 🎯 Task
- Make a to-do list program
- Allow user to add, view, remove tasks

---

## 📅 Day 6: Dictionaries – Key to Python

### 🔍 What You'll Learn
- Dictionary creation & access
- Loops with dicts

### 🛠️ Let's Do It
```python
person = {"name": "Bob", "age": 25}

print(person["name"])

```
### Add to python dictionary
```python

person = {"name": "Bob", "age": 25}

## Added key profession and value engineer

person["profession"]="engineer"
print(person)

```
### Remove 
```python

person = {"name": "Bob", "age": 25}
# this will remove any key randomly and value.
person.popitem()

print(person)

```
#### The del keyword removes the item with the specified key name

```python

 person = {"name": "Bob", "age": 25}
del person["name"]

print(person)


output

person = {"age": 25}

```
### Loop Map
```python

 person = {"name": "Bob", "age": 25}
for key,val in fruits:
  print(key)
    print(" val ")
       print(val)
  
```


### 🎯 Task
- Create a phonebook: name → number
- Allow user to add and search contacts

---

## 📅 Day 7: Tuples, Sets, and Data Types

### 🔍 What You'll Learn
- Tuples (immutable lists)
- Sets (unique unordered items)
- Type conversions

### 🛠️ Let's Do It
```python
# Tuple
point = (10, 20)
print(point[0])

# Set
colors = {"red", "blue", "red"}
print(colors)  # Only unique values

# Type casting
num = "5"
print(int(num) + 1)
```

### 🎯 Task
- Create a set of user-entered numbers (avoid duplicates)
- Try storing multiple (x, y) positions as tuples

---

## 📅 Day 8: File Handling

### 🔍 What You'll Learn
- Reading and writing files
- Using `with open(...)` safely

### 🛠️ Let's Do It
```python
# Write
with open("notes.txt", "w") as f:
    f.write("This is a note.")

# Read
with open("notes.txt", "r") as f:
    print(f.read())
```

### 🎯 Task
- Save a user’s to-do list to a file
- Allow them to read it later

---

## 📅 Day 9: Error Handling & Debugging

### 🔍 What You'll Learn
- `try`, `except`, `finally`
- Debugging techniques

### 🛠️ Let's Do It
```python
try:
    num = int(input("Enter a number: "))
    print(10 / num)
except ZeroDivisionError:
    print("Can't divide by zero!")
except ValueError:
    print("Please enter a valid number.")
```

### 🎯 Task
- Create a calculator that handles divide-by-zero and bad input

---

## 📅 Day 10: Build a Mini Project 🎉

### 🧠 Combine Everything You've Learned

### Project Idea: Contact Book App
- Add, search, and save contacts using a dictionary
- Use functions to organize your code
- Save/load from a file

```python
# Starter idea
def add_contact(name, number, contacts):
    contacts[name] = number

def search_contact(name, contacts):
    return contacts.get(name, "Not found")
```

🎯 Your Goal:  
- Make it menu-driven  
- Add error handling  
- Save/load to a file

---

### 🏁 You're Done!
You've built real things. Now keep going:
- Try small apps (calculator, quiz game, chatbot)
- Explore libraries: `random`, `datetime`, `matplotlib`

Happy coding 🚀
