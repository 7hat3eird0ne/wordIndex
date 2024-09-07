WIP

Currently this lets users get a unique index from any strings of arbitary characters and translate back using said index

For example, if we set the arbitary characters to be a normal english alphabet with no other characters in exact same order (meaning 26 characters), the first few indexes are like this:

0\. ""

1\. "a"

2\. "b"

3\. "c"

...

26\. "z"

27\. "aa"

28\. "ba"

...

etc, this way it keeps incrementing, going to infinity, the scale of number scales with the length of string too

- the core math behnid this is converting every character into integer, going from 0 up to (amount of characters)-1 (in our case 25), then we use the integers as digits, with base of the amount of possible characters there

- so for example "code" could be written as this in base 26:
    - 4 3 14 2

- next, after we got this represantion, we add this little piece of math doing the magic, assuming l = length of string and n = number of avaible characters (in our case 26):

    - n\*\*l - (n - 2) \* (n\*\*x - 1) / (n - 1) - 1
    - if you want to derive this little formula i found on airplane, you can try to add a 1 on new digit place with biggest value to remove length ambuguity, and then try to find a summation of the skips between biggest value of one length and smallest value of next length (and simplify the summation), good luck

the code is customisable, allowing people to change the character order, using a valid json (just look at the default one and try to learn it, i plan to add a small guide through it later)

- currently, it supports:
    - changing the characters order, duh (order)
    - changing the way it adds characters so they go in reverse (reverseAppend) 
        - for example if there was an index which used to give you string "abcd" it will give you now "dcba", this settings allows jsons to exist, which when the string includes only numbers, its index will be identical to the number in the string
    - removing indexs smaller than a certain length (minLen)
        - so for example if we make minLen equal 1, it will get rid of the empty string "", meaning that because it is missing now, the string "a" will have index 0 instead of 1
    - make it case insensitive (caseSensitive)
        - if it will be false, it will make every character in the JSON
- settings which are not supported and may (or may not) be supported in future:
    - excluding or including certain characters on certain positions
        - so for example strings starting with "_" dont get an index and instead the next valid string after it would get the index
        - sadly this would make the calculations in math a bit annoying, as i would have to go unsimplify the hidden summation used in the formula (which was removed by simplifying) and add variances into it
        - as of now i dont feel like making it, as i explained earlier, but i may look into it in future if i wont forget about this project