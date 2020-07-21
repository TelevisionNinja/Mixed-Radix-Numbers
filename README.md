# Multi-Base-Numbers
A little module for working with multi base numbers like time.

An example would be 1:20 + 2 hours and 41 mins = 4:01 or how it is represented in the code, [1, 20] + [2, 41] = [4, 1].

Numbers are prepresented as lists, so 10 and -99 would need to be converted into [1, 0] and [-9, 9].

For numbers with established representations like hexadecimal where 10 = a, there is no such representation in this code. All the values are represented as their decimal equivalent. To work with hexadecimal, for example, the numbers would have to be converted from [2, A, B] to [2, 10, 11]. The reason is to allow for massive bases like base 9,000 since there isn't really a single character representation for 9,000.
