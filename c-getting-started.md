---
layout: page
title: C Getting Started — Hands On
permalink: /c-getting-started/
---

# C Getting Started — Hands On

Learn **C by typing and running code**, not by watching theory.  
Each section has a short explanation, a runnable example, and a **Task** you must complete before moving on.

**Time:** 1–2 days (focused)  
**You need:** a C compiler (`gcc` or `clang`) and a text editor (VS Code / Cursor / Notepad++)

**Related:** [C++ STL for CP](/cpp-stl/) · [Courses](/courses/)

---

## Table of Contents

1. [Install & Hello World](#1-install--hello-world)  
2. [Variables & Types](#2-variables--types)  
3. [Input & Output](#3-input--output)  
4. [Operators](#4-operators)  
5. [if / else](#5-if--else)  
6. [Loops](#6-loops)  
7. [Arrays](#7-arrays)  
8. [Functions](#8-functions)  
9. [Pointers (Basics)](#9-pointers-basics)  
10. [Strings (char arrays)](#10-strings-char-arrays)  
11. [Structs](#11-structs)  
12. [Mini Projects](#12-mini-projects)  
13. [Cheat Sheet](#13-cheat-sheet)

---

## 1. Install & Hello World

### Windows
1. Install [MinGW-w64](https://www.mingw-w64.org/) or use **MSYS2** / **WinLibs**.  
2. Confirm in terminal:

```bash
gcc --version
```

### macOS
```bash
xcode-select --install
clang --version
```

### Linux
```bash
sudo apt update && sudo apt install build-essential
gcc --version
```

### Your first program

Create `hello.c`:

```c
#include <stdio.h>

int main(void) {
    printf("Hello, C!\n");
    return 0;
}
```

Compile and run:

```bash
gcc hello.c -o hello
./hello
```

Windows:

```bash
gcc hello.c -o hello.exe
hello.exe
```

**What each line means**

| Line | Meaning |
|---|---|
| `#include <stdio.h>` | Pull in standard I/O (printf, scanf) |
| `int main(void)` | Program entry point |
| `printf(...)` | Print text |
| `\n` | Newline |
| `return 0;` | Exit successfully |

### Task 1
Change the message to print your name and today’s date on two lines.

---

## 2. Variables & Types

```c
#include <stdio.h>

int main(void) {
    int age = 20;
    float height = 5.9f;
    double pi = 3.1415926535;
    char grade = 'A';
    long long big = 10000000000LL;

    printf("age=%d height=%.1f grade=%c big=%lld\n",
           age, height, grade, big);
    return 0;
}
```

### Common types (CP / systems)

| Type | Typical size | Format specifier |
|---|---|---|
| `char` | 1 byte | `%c` |
| `int` | 4 bytes | `%d` |
| `long long` | 8 bytes | `%lld` |
| `float` | 4 bytes | `%f` |
| `double` | 8 bytes | `%lf` (scanf) / `%f` or `%lf` (printf) |
| `unsigned int` | 4 bytes | `%u` |

**Rules**
- Declare before use (in older C) — still good habit.  
- Prefer `long long` for large integers in problems.  
- `=` is assignment; `==` is comparison (next sections).

### Task 2
Declare `int a = 7`, `int b = 3`. Print their sum, difference, and product.

---

## 3. Input & Output

```c
#include <stdio.h>

int main(void) {
    int a, b;
    printf("Enter two integers: ");
    scanf("%d %d", &a, &b);
    printf("Sum = %d\n", a + b);
    return 0;
}
```

**Important:** `scanf` needs **addresses** → `&a`, `&b`.

Read a single character (skip leftover newline carefully later):

```c
char ch;
scanf(" %c", &ch);  /* leading space skips whitespace */
```

### Task 3
Read three integers and print their average as a `float` with 2 decimal places:

```c
printf("%.2f\n", avg);
```

---

## 4. Operators

```c
int a = 10, b = 3;

a + b;  a - b;  a * b;
a / b;   /* 3  (integer division) */
a % b;   /* 1  (remainder) */

a += 2;  /* a = a + 2 */
a++;     /* post-increment */
++a;     /* pre-increment */

/* Relational */
a == b; a != b; a < b; a <= b; a > b; a >= b;

/* Logical */
(a > 0) && (b > 0);
(a > 0) || (b > 0);
!(a == b);
```

### Task 4
Read an integer `n`. Print whether it is even or odd using `%`.

---

## 5. if / else

```c
#include <stdio.h>

int main(void) {
    int marks;
    scanf("%d", &marks);

    if (marks >= 90) {
        printf("Grade A\n");
    } else if (marks >= 75) {
        printf("Grade B\n");
    } else if (marks >= 50) {
        printf("Grade C\n");
    } else {
        printf("Fail\n");
    }
    return 0;
}
```

### Nested example

```c
if (x > 0) {
    if (x % 2 == 0) printf("positive even\n");
    else printf("positive odd\n");
} else {
    printf("non-positive\n");
}
```

### Task 5
Read year `y`. Print `Leap` if leap year, else `Not leap`.  
Rule: divisible by 400, OR (divisible by 4 and not by 100).

---

## 6. Loops

### `for`

```c
for (int i = 1; i <= 5; i++) {
    printf("%d ", i);
}
```

### `while`

```c
int n = 5;
while (n > 0) {
    printf("%d ", n);
    n--;
}
```

### `do-while` (runs at least once)

```c
int x;
do {
    scanf("%d", &x);
} while (x <= 0);
```

### Classic: sum 1..n

```c
int n, sum = 0;
scanf("%d", &n);
for (int i = 1; i <= n; i++) sum += i;
printf("%d\n", sum);
```

### Task 6
1. Print the multiplication table of a number `k` (1..10).  
2. Read `n`, print factorial of `n` (use `long long`).

---

## 7. Arrays

```c
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    int a[1000];           /* fixed max size — common beginner style */

    for (int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
    }

    int mx = a[0];
    for (int i = 1; i < n; i++) {
        if (a[i] > mx) mx = a[i];
    }
    printf("Max = %d\n", mx);
    return 0;
}
```

**Notes**
- Index starts at `0`.  
- `a[n]` is out of bounds if size is `n` (valid indices `0..n-1`).  
- For large `n`, prefer global arrays or dynamic allocation later.

### Reverse print

```c
for (int i = n - 1; i >= 0; i--) printf("%d ", a[i]);
```

### Task 7
Read `n` and an array. Print:
1. Sum of elements  
2. Count of even numbers  
3. The array sorted ascending (bubble sort is fine for learning)

Bubble sort sketch:

```c
for (int i = 0; i < n; i++) {
    for (int j = 0; j + 1 < n - i; j++) {
        if (a[j] > a[j + 1]) {
            int t = a[j];
            a[j] = a[j + 1];
            a[j + 1] = t;
        }
    }
}
```

---

## 8. Functions

```c
#include <stdio.h>

int add(int x, int y) {
    return x + y;
}

void greet(void) {
    printf("Hi from a function!\n");
}

int main(void) {
    greet();
    printf("%d\n", add(2, 3));
    return 0;
}
```

### Pass by value (default)

```c
void try_change(int x) {
    x = 100;   /* does NOT change caller's variable */
}
```

To modify a caller’s variable, pass a **pointer** (next section).

### Task 8
Write:
- `int is_prime(int n)` → return 1 if prime, else 0  
- In `main`, read `n` and print `Prime` / `Not prime`

---

## 9. Pointers (Basics)

A pointer stores a **memory address**.

```c
#include <stdio.h>

int main(void) {
    int x = 10;
    int *p = &x;     /* p points to x */

    printf("x=%d\n", x);
    printf("address=%p\n", (void*)p);
    printf("value via pointer=%d\n", *p);

    *p = 25;         /* change x through p */
    printf("x now=%d\n", x);
    return 0;
}
```

### Swap with pointers

```c
void swap(int *a, int *b) {
    int t = *a;
    *a = *b;
    *b = t;
}

int main(void) {
    int x = 3, y = 7;
    swap(&x, &y);
    printf("%d %d\n", x, y);  /* 7 3 */
    return 0;
}
```

### Array ↔ pointer

```c
int a[5] = {1, 2, 3, 4, 5};
int *p = a;          /* same as &a[0] */
printf("%d\n", p[2]); /* 3 */
```

### Task 9
Write `void increment(int *x)` that adds 1 to the caller’s variable. Test it from `main`.

---

## 10. Strings (char arrays)

In C, a string is a `char` array ending with `'\0'`.

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char name[100];
    scanf("%s", name);          /* reads until whitespace; no & needed */
    printf("Hello, %s\n", name);
    printf("Length = %zu\n", strlen(name));
    return 0;
}
```

### Common `<string.h>` functions

```c
strlen(s);
strcpy(dest, src);
strncpy(dest, src, n);
strcmp(a, b);     /* 0 if equal */
strcat(dest, src);
```

### Read a full line (with spaces)

```c
char line[200];
fgets(line, sizeof(line), stdin);
```

### Task 10
1. Read a word; print it reversed.  
2. Read two words; print whether they are equal (`strcmp`).

Reverse sketch:

```c
int n = strlen(s);
for (int i = 0; i < n / 2; i++) {
    char t = s[i];
    s[i] = s[n - 1 - i];
    s[n - 1 - i] = t;
}
```

---

## 11. Structs

Group related data:

```c
#include <stdio.h>

struct Student {
    char name[50];
    int roll;
    float marks;
};

int main(void) {
    struct Student s;
    scanf("%s %d %f", s.name, &s.roll, &s.marks);
    printf("%s %d %.2f\n", s.name, s.roll, s.marks);
    return 0;
}
```

### Array of structs

```c
struct Student class[100];
class[0].roll = 1;
```

### Task 11
Define `struct Point { int x, y; }`.  
Read two points and print the Manhattan distance `|x1-x2| + |y1-y2|`.

---

## 12. Mini Projects

Build these in separate `.c` files. No libraries beyond `stdio.h` / `string.h` / `math.h`.

### Project A — Calculator
Menu:
1. Add  2. Subtract  3. Multiply  4. Divide  5. Exit  
Loop until exit. Guard divide-by-zero.

### Project B — Number Guessing
Program picks a fixed secret (e.g. `42`) or uses a simple formula.  
User guesses until correct; print attempt count.

### Project C — Student Marks Manager
Store up to 50 students (`struct`). Menu:
- Add student  
- Display all  
- Find by roll  
- Average marks  

### Project D — Mini Array Toolkit
Read `n` and array, then menu:
- Sum / Max / Min  
- Linear search  
- Reverse  
- Sort  

### Done checklist
- [ ] All Task 1–11 completed and run successfully  
- [ ] At least **two** mini projects working  
- [ ] You can explain what `&` and `*` do in one sentence each  

---

## 13. Cheat Sheet

```c
/* compile */
gcc file.c -o app && ./app

/* io */
printf("%d %lld %f %c %s\n", i, ll, d, ch, str);
scanf("%d", &i);
scanf("%s", str);

/* loops */
for (int i = 0; i < n; i++) { }
while (cond) { }

/* array */
int a[100];
a[i] = x;

/* pointer */
int *p = &x; *p = 5;

/* string */
char s[100]; strlen(s); strcmp(a,b);
```

### Common beginner bugs

| Bug | Fix |
|---|---|
| Forgot `&` in `scanf` for `int` | `scanf("%d", &x);` |
| Used `&` with `%s` | `scanf("%s", s);` — no `&` |
| `=` instead of `==` in if | Use `==` |
| Array out of bounds | Valid indices `0..n-1` |
| Integer division surprise | `5/2` is `2`; use floats if needed |
| Missing `\0` / overflow string | Keep buffer size larger than input |

---

## What’s Next?

- Competitive programming in C++: [C++ STL Hub](/cpp-stl/)  
- More practice: [DSA Cheatsheet](/dsa-cheatsheet/)  
- All courses: [Courses](/courses/)

---

*Type every example. Break it on purpose. Fix it. That is how C clicks.*
