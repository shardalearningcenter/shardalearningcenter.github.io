# 1. Standard Binary Search
Find an exact element in a sorted array.

## 🔧 Adjustments
If midVal < target: low = mid + 1

If midVal > target: high = mid - 1

## ✅ Use When:
You need to check if an element exists in a sorted array.

## 🧠 Java Code

```
int binarySearch(int[] arr, int target) {
    int low = 0, high = arr.length - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1; // not found
}

```
## 🧭 2. Lower Bound (First Element ≥ Target)
### 🔧 Adjustments
If arr[mid] < target: low = mid + 1

Else: high = mid - 1

### ✅ Use When:
You need the first element ≥ target (e.g., start of range).

### 🧠 Java Code
```int lowerBound(int[] arr, int target) {
    int low = 0, high = arr.length - 1, ans = arr.length;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] >= target) {
            ans = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    return ans;
}
```

## ⛳ 3. Upper Bound (First Element > Target)

### 🔧 Adjustments
If arr[mid] <= target: low = mid + 1

Else: high = mid - 1

### ✅ Use When:
You want to find the first element greater than the target.

### 🧠 Java Code

```
int upperBound(int[] arr, int target) {
    int low = 0, high = arr.length - 1, ans = arr.length;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] > target) {
            ans = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    return ans;
}
```

## 🔁 4. Find First Occurrence of Duplicate Element
### 🔧 Adjustments
If arr[mid] == target: update ans = mid and search left (high = mid - 1)

Else standard binary search logic.

### ✅ Use When:
Duplicates exist, and you want the first index of the target.

### 🧠 Java Code

```
int firstOccurrence(int[] arr, int target) {
    int low = 0, high = arr.length - 1, ans = -1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) {
            ans = mid;
            high = mid - 1;
        } else if (arr[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return ans;
}
```

## 🧮 5. Find Last Occurrence of Duplicate Element
### 🔧 Adjustments
If arr[mid] == target: update ans = mid and search right (low = mid + 1)

Else standard binary search logic.

### ✅ Use When:
Duplicates exist, and you want the last index of the target.

### 🧠 Java Code
```
int lastOccurrence(int[] arr, int target) {
    int low = 0, high = arr.length - 1, ans = -1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) {
            ans = mid;
            low = mid + 1;
        } else if (arr[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
   
    return ans;
}
```

## 🎯 Summary Table

# Binary Search Variants Cheat Sheet

This table summarizes the most common binary search patterns, what conditions to check, how to adjust the search space, and what each variant is used for.

| Variant           | Condition at `mid`       | Adjust `low` or `high`        | Goal                  |
|-------------------|---------------------------|-------------------------------|------------------------|
| Exact Match       | `arr[mid] == target`      | `low = mid + 1` or `high = mid - 1` | Find element index     |
| Lower Bound       | `arr[mid] >= target`      | `high = mid - 1`              | First ≥ target         |
| Upper Bound       | `arr[mid] > target`       | `high = mid - 1`              | First > target         |
| First Occurrence  | `arr[mid] == target`      | `high = mid - 1`              | Leftmost match         |
| Last Occurrence   | `arr[mid] == target`      | `low = mid + 1`               | Rightmost match        |

## Notes

- **Lower Bound**: Useful for finding where an element can be inserted without breaking the sort order.
- **Upper Bound**: Helps in range queries, e.g., count of elements equal to a value.
- These patterns assume the array is **sorted in ascending order**.


Let me know if you want binary search on rotated sorted arrays, peak elements, or 2D matrices next.








You said:
whats lower bound upper cound meaning


ChatGPT said:
Great question!

📌 Lower Bound and Upper Bound are binary search variants used to find the position (not necessarily the exact match) of elements in a sorted array.
🔽 Lower Bound
❓ What it means:
The index of the first element that is greater than or equal to the target.

✅ Use when:
You want to find the starting point of a range, or check how many elements are less than the target.

🔍 Example:
java
Copy
Edit
int[] arr = {2, 4, 4, 4, 6, 8};
int target = 4;

// Lower bound of 4 is index 1 (first 4)
🔼 Upper Bound
❓ What it means:
The index of the first element that is strictly greater than the target.

✅ Use when:
You want to find the ending point of a range, or count how many elements are less than or equal to the target.

🔍 Example:
java
Copy
Edit
int[] arr = {2, 4, 4, 4, 6, 8};
int target = 4;

// Upper bound of 4 is index 4 (first element > 4, which is 6)
🔁 Real-world Use Case:
Say you're counting how many times target = 4 appears:

java
Copy
Edit
count = upperBound(arr, 4) - lowerBound(arr, 4);
// = 4 - 1 = 3
🧠 Visualization:
For arr = {2, 4, 4, 4, 6, 8} and target = 4:

makefile
Copy
Edit
Indexes:      0  1  2  3  4  5
Values:       2  4  4  4  6  8
                 ↑     ↑
              LB=1   UB=4
