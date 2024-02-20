# rev/glottem

## Uncovering what to do
The flavor text reads:

> Haha glottem good!
>
> Note: The correct flag is 34 characters long.

Knowing that flags are of the format `lactf{<message>}`, we can infer that the `<message>` is 34 - 7 = 27 characters long.

Next, we look at the script. We are immediately greeted with a massive array `e`:
```javascript
e = [[[14,13,17,10,14,12,16,16,13,11,17,13,14,14,12,14,15,13,12,17,16,12,17,13,14,12,16],[14,14,...
```
We know that this is some 3-dimensional array, because `e` starts with three opening braces. We also notice that the values in the array are between 10 and 17.

 We examine what comes after the array (with several things omitted because I simply ignored them [lmao](#hashing)):

```javascript
alpha="abcdefghijklmnopqrstuvwxyz_"
d=0;s=argv[1];
for i in range(6,len(s)-2):
    d+=e[i-6][alpha.index(s[i])][alpha.index(s[i+1])]
exit(+(d!=260,[d!=61343])[0])
```

It's clear that the script is using the array to perform some operation on our input string. 
Firstly, the for loop starts at 6.
Remembering that the input string is of the form `lactf{<message>}`, `i` iterates starting from the index of the first character of `<message>`, which is index 6.

So, we know that the `for` loop does some operation on `<message>`.

Inside the `for` loop, we see what the array is being used for: given an index, the character at that index, and the next character, the array gives an integer to add to `d`.

For example, the value of `d` on the input `"lactf{hello}"` would be:

```javascript
d = 
e[0]['h']['e']+
e[1]['e']['l']+
e[2]['l']['l']+
e[3]['l']['o']
```
(I handwave the `alpha.index()` call for clarity).

Notice that the number of iterations is `len(message) - 1`.

Finally, the last line makes the program exit with nonzero status if `d != 260`. We want it to exit successfully (with status 0), so we need to make `d == 260`. 

In other words, we need to find a `<message>` that makes `d == 260`. Since the values in the array take on the values from 10 to 17, and the loop runs 27-1 = 26 times, the only way for `d` to be 260 is if **we only use the 10s in the array**.

## Finding the message

(This problem feels pretty algorithmic, so I first coded up a solution in C++. I used some fancy typedef and lambda templates that I typically use in competitive programming contests, but most people don't have those. So, I will instead show an implementation in Python.)

In a Python script, we first define `e` and `alpha`:
```python
e = [[[...]]] # just copy paste the thing in the glottem script lol

alpha="abcdefghijklmnopqrstuvwxyz_"
```
Let's quickly print out the dimensions of `e`, as a sanity check:
```python
print(f"{len(e)} by {len(e[0])} by {len(e[1])}")
```
```
26 by 27 by 27
```
OK, this makes sense; the loop runs 26 times, and `alpha` is 27 characters long.

Next, we need to filter away everything but the 10s.
Basically, given an index and a character at the index, we only care about the next characters that correspond to a 10:

```python
# mat[i][j] returns a list of valid characters to continue the string with
mat = [[[] for _ in range(27)] for _ in range(26)]
for i in range(len(e)):
    for j in range(len(e[i])):
        for k in range(len(e[i][j])):
            if e[i][j][k] == 10:
                mat[i][j].append(k)
```

Algorithmically speaking, `mat` represents a forest. Each node corresponds to (i, j), and every `k` in `mat[i][j]` corresponds to the child (i + 1, k). We want to find the paths from a root to a leaf at (26, L) for some L.

We achieve this with a DFS search down the trees, which has a concise recursive implementation:
```python
def solve(start_char, string):
    if len(string) >= 26:
        print(string + alpha[start_char])
        return

    for child in mat[len(string)][start_char]:
        solve(child, string + alpha[start_char])
```
Finally, we run `solve()` on the roots of the trees:
```python
for c in range(len(alpha)):
    solve(c, "")
```

Running this gives quite a few strings! It is helpful to redirect this output to a file for examination, like so:

```
$ python glottem.py >output.txt
```

We see that there are more than 42000 strings! How are we going to find the flag? There's two ways: we can either use English, or we can use hashing[***](#hashing).

### Just use English
In `output.txt`, we search through the strings.
We pretty quickly notice `..._free_deal` suffixes and `_two_free` substrings in some of the strings.

This means that the flag message is some English phrase. Using a text search (like ctrl+f) for `_two_free_deal` a few times gets us to
`colve_one_get_two_free_deal`. 

Hmm.

"Colve" isn't a real word. But "solve" is! The flag message is probably `solve_one_get_two_free_deal`. As a sanity check, we see that this flag is indeed in `output.txt`.

We submit `lactf{solve_one_get_two_free_deal}` and rejoice.

### ***Hashing
The previous sections detailed how I managed to get a second solve on this challenge (although I did the coding in C++, not in Python). I happened to ignore an important part of the challenge, instead choosing to rely on my **supreme English and pattern recognition skills**.

Let's use the stuff I ignored. The unadulterated code after the definition of `e` is:
```javascript
alpha="abcdefghijklmnopqrstuvwxyz_"
d=0;s=argv[1];1//1;"""
/*"""
#*/for (let i = 0; i < s.length; i ++) {/*
for i in range(6,len(s)-2):
    #*/d=(d*31+s.charCodeAt(i))%93097/*
    d+=e[i-6][alpha.index(s[i])][alpha.index(s[i+1])]#*/}
exit(+(d!=260,[d!=61343])[0])
4201337
```

Hopefully, the text highlighting shows the interleaved code. It's a string hasher! It takes in `lactf{<message>}` and hashes it, and it wants it to match `61343`. Quickly modifying the python script to save strings instead of print them:

```python
strings = []
def solve(start_char, string):
    if len(string) >= 26:
        # print(string + alpha[start_char])
        strings.append(string + alpha[start_char])
        return

    for child in mat[len(string)][start_char]:
        solve(child, string + alpha[start_char])
```

And then, we rewrite the hasher in Python and hash every string, searching for hash of 61343:

```python
def hash(string):
    d = 0
    flag = "lactf{" + string + "}"
    for i in range(len(flag)):
        d=(d*31 + ord(flag[i]))%93097
    return d

for s in strings:
    if hash(s) == 61343:
        print(s)
```

Running our full script now gives:

```
$ python glottem.py
26 by 27 by 27
solve_one_get_two_free_deal
```

That's our flag!

The full script can be found in `glottem.py`.