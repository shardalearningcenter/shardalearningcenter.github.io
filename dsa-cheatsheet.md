# Snippets which will be useful

## Custom comparator 
Say you have been given task to sort elements based on diffrence between the input element and the number in the list
So write this oneliner and you can sort the element.

```
 Collections.sort(ls, 
        (n1, n2) -> Math.abs(n1 - x) - Math.abs(n2 - x));
```
### There is another method to compare the strings it is called compareTo()
```
string1.compareTo(string2)
```
