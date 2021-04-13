# Exercise 1

We could set `{x = 2}`. That would still make `{ z > 1}` valid


# Exercise 2
```
{true}
b = 2 -a
{ b = 2, a = 0}
c = 2 *b
{ b= 2, c = 4}
d = c + 1
{d = 5, c = 4, b = 2}
```

Since d = 5 and d = c+1, we have c=4
Since c = 4 and c = 2b , b =2 
Since b = 2 and b = 2 - a, a = 0

# Exercise 3

```
{ x > 0}
y = (x/2)  * 2
{(x is odd) => y=x-1 and (x is even) => y=x }
z = x - y
{(x is odd) => z = x - (x-1) = -1 and (x is even) => z = x- x = 0  }
a = 5z + (1-z)*12
{(x is odd) => a = 5(-1) + (1- (-1))*12=5 and (x is even) => a = 5*(0) +(1-0)*12=12 }
```

# Exercise 4

```
d = ...
- {a>=0 --> d = 0 & a<0 --> d = 1 }
- m = 2d + 3(1-d)
- {a>=0 --> d = 0 & a <0 --> d = 1;
   d = 0 --> m = 3 ; d = 1 --> m = 2;
  }
- x = 2b
- {a>=0 --> d = 0 & a <0 --> d = 1;
   d = 0 --> m = 3 ; d = 1 --> m = 2;
   x = 2b
  }
- x = 2x
  {a>=0 --> d = 0 & a <0 --> d = 1;
   d = 0 --> m = 3 ; d = 1 --> m = 2;
   x = 4b
  }et
- x = mx
  {a>=0 --> d = 0 & a <0 --> d = 1;
   d = 0 --> m = 3 & d = 1 --> m = 2;
   m = 3 --> x = 12b & m = = --> x = 8b
  }
- x = x + 1
  {a>=0 --> d = 0 & a <0 --> d = 1;
   d = 0 --> m = 3 & d = 1 --> m = 2;
   a>=0 --> x = 12b + 1 & a<0 --> x = 8b + 1
  }
```

This code contains a conditional because all subsequent calculations
depend on the value of `a`: `d`, `m` and `x`

# Exercise 5

```
d = ...
- {d < 2}
- m = 2d + 3(1-d)
- { m > 1 ; d < 2}
- x = 2b
- { m > 1 ; x = 2b}
- x = 2x
  { m > 1 ; x = 4b}
- x = mx
  { m > 1 ; x > 4b}
- x = x + 1
  { m > 1 ; x > 4b+1}
```

I  chose `{d < 2}` because although its value depends on `a`, its value
is either 0 or 1


> Think about a codebase you've worked on recently. Find a function
> that knows some fact related to a different module of the system,
> through some mechanism other than direct reference. How does it do
> so? Post your answer as a comment. 

