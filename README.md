# About
Hello, currrently, this repository allows users to assign a unique index to any string, with the index scaling up with the length of the string

For example, lets make our character set, which is pretty much a json file with all settings and order of characters, we don't have to care about the setting that much, lets just say the characters are only lowercase english alphabet letters in the same order as in alphabet

The first few indexes of our character set would be:

- 0\. ""
- 1\. "a"
- 2\. "b"
- 3\. "c"
- ...
- 26\. "z"
- 27\. "aa"
- 28\. "ba"
- ...

and so on...

## The math behind it

The way the number is actualy computed and the math behind it is pretty simple:

1. First we convert every individual character in the string to a digit from 0 to N-1 where N is the amount of characters in character set, we can just say that it is the index of the character in the list
1. Then we put them together and convert the number represenation to the decimal base
    - For example, string "code" in our alphabet character set could be written as 
    4(e) 3(d) 14(o) 2(c)
    - which converted to decimal ends up becoming 72698
1. Because adding "a" or any character which is first in character set ends up adding 0 to it, it is hard to know if the index refferences to version with or without additional a's, we can fix that by adding N**L, where ** is exponation and L is length of string (for "code", L is 4)
1. Because of the additional N**L, the formula now leaves out few indexes, the two strings (in their numerical represenation) in between which are the skipped indexes always look like this (where M = N-1):
    - 1MM and 1000 (add additional M's and 0's to reflect any length)
    - if we change the forms into their decimal ones:
        - 1MM = 2N**(L-1)
        - 1000 = N**(L)
    - and take difference between them, and subtract 1, we can get the value we should have to remove the additional index:
        - N**(L) - 2N**(L-1)
    - Now we gotta take summation of it from 0 to L, but because 0 gives wrong value instead of 1, we just manualy subtract 1 manualy and make the summation starts at 1, this gives us our final formula which we add to numerical representation instead of just alone N**l:
        - N\*\*L - sum( N\*\*(j) - 2N\*\*(j-1) , where j = 1 -> L) - 1
1. We can simplify the summation though
    1. first we change the inside of summation to a multiplication 
        - (1 - 2/N) \* (N\*\*j) 
    1. then we can take out the (1 - 2/N) bit out of the summation
    1. then we can add one to j everywhere so that the bounds get lowered by one
        - sum( N\*\*(j+1) , where j = 0 -> L-1)
    1. then we can multiply the inner summation bit by (N-1) and divide by it the entire summation
    1. then we can simplify the summation so that it is:
        - N**(L+1) - 1
    1. we can also multiply the thing by N so we can get rid of the (+1) in the exponent, and simplify the (1 - 2/N)

1. then we get subtract the result addition thing and subtract it from our numerical representation and we get our result formula:
    - index = numRepres + N\*\*L - (N - 2) \* (N\*\*L - 1) / (N-1) - 1

## Customisation

We can customise the calculator a bit, by copying the json file and changing the following:
- the 'order' array defines in which order do the characters go, every element has to be a string of length 1, duplicates can be there but can make the indexes inaccurate so I don't recomend them
- the 'reverseAppend' bool says whatever the append should be reversed, for example "code" will normaly be 4 3 14 2, but with reverse append it will be reversed
- the 'minLen' integer says what should be the minimal length avaible, this just subtracts the final index by the smallest index of the minimal length, for example if we make minLen = 2, it will make "aa" turn into 0, instead of being 27
- the 'caseSensitive' bool says whatever it should be case sensitive or not, if it is set to false, it will just turn everything lowercase

This is most probably everything for now. Feel free to use it if it can be remotely usable in your case, just credit me somewhere visible

Thank you for reading!