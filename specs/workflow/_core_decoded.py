i
m
p
o
r
t
 
o
s




D
I
R
 
=
 
'
E
:
\
�
�
�
�
�
�
�
�
�
\
�
�
�
�
�
�
\
A
t
l
a
s
\
s
p
e
c
s
\
w
o
r
k
f
l
o
w
'


o
s
.
m
a
k
e
d
i
r
s
(
D
I
R
,
 
e
x
i
s
t
_
o
k
=
T
r
u
e
)


N
L
 
=
 
c
h
r
(
1
0
)


T
Q
 
=
 
c
h
r
(
3
9
)
 
*
 
3


B
T
 
=
 
c
h
r
(
9
6
)
 
*
 
3




D
E
P
S
 
=
 
[


 
 
 
 
'
R
F
C
-
0
0
0
1
 
R
u
n
t
i
m
e
 
O
v
e
r
v
i
e
w
'
,


 
 
 
 
'
R
F
C
-
0
0
0
2
 
R
u
n
t
i
m
e
 
L
i
f
e
c
y
c
l
e
'
,


 
 
 
 
'
R
F
C
-
0
0
0
3
 
R
u
n
t
i
m
e
 
S
e
r
v
i
c
e
 
M
o
d
e
l
'
,


 
 
 
 
'
R
F
C
-
0
0
0
4
 
R
u
n
t
i
m
e
 
S
c
h
e
d
u
l
e
r
'
,


 
 
 
 
'
R
F
C
-
0
0
0
5
 
R
u
n
t
i
m
e
 
E
v
e
n
t
 
B
u
s
'
,


 
 
 
 
'
R
F
C
-
0
0
0
6
 
R
u
n
t
i
m
e
 
S
t
a
t
e
 
M
a
n
a
g
e
m
e
n
t
'
,


 
 
 
 
'
R
F
C
-
1
0
0
1
 
C
o
m
m
o
n
 
E
v
e
n
t
 
M
o
d
e
l
'
,


 
 
 
 
'
R
F
C
-
1
0
0
2
 
C
o
m
m
o
n
 
S
t
a
t
e
 
M
o
d
e
l
'
,


 
 
 
 
'
R
F
C
-
1
0
0
3
 
C
o
m
m
o
n
 
C
a
p
a
b
i
l
i
t
y
 
M
o
d
e
l
'
,


 
 
 
 
'
R
F
C
-
1
0
0
4
 
C
o
m
m
o
n
 
C
o
n
t
r
a
c
t
 
M
o
d
e
l
'
,


 
 
 
 
'
R
F
C
-
1
0
0
5
 
C
o
m
m
o
n
 
M
a
n
i
f
e
s
t
 
M
o
d
e
l
'
,


 
 
 
 
'
R
F
C
-
1
0
0
6
 
C
o
m
m
o
n
 
E
r
r
o
r
 
M
o
d
e
l
'
,


]




R
E
L
 
=
 
{
}


f
o
r
 
_
i
,
 
_
n
 
i
n
 
[


 
 
 
 
(
3
0
1
,
'
O
v
e
r
v
i
e
w
'
)
,


 
 
 
 
(
3
0
2
,
'
L
a
n
g
u
a
g
e
'
)
,


 
 
 
 
(
3
0
3
,
'
E
x
e
c
u
t
i
o
n
'
)
,


 
 
 
 
(
3
0
4
,
'
R
u
n
t
i
m
e
'
)
,


 
 
 
 
(
3
0
5
,
'
L
i
f
e
c
y
c
l
e
'
)
,


 
 
 
 
(
3
0
6
,
'
S
t
a
t
e
'
)
,


 
 
 
 
(
3
0
7
,
'
C
o
n
t
e
x
t
'
)
,


 
 
 
 
(
3
0
8
,
'
E
v
e
n
t
s
'
)
,


 
 
 
 
(
3
0
9
,
'
A
c
t
i
o
n
s
'
)
,


 
 
 
 
(
3
1
0
,
'
C
o
n
d
i
t
i
o
n
s
'
)
,


 
 
 
 
(
3
1
1
,
'
T
r
i
g
g
e
r
s
'
)
,


 
 
 
 
(
3
1
2
,
'
S
c
h
e
d
u
l
e
r
'
)
,


 
 
 
 
(
3
1
3
,
'
P
a
r
a
l
l
e
l
i
s
m
'
)
,


 
 
 
 
(
3
1
4
,
'
E
r
r
o
r
 
H
a
n
d
l
i
n
g
'
)
,


 
 
 
 
(
3
1
5
,
'
R
e
c
o
v
e
r
y
'
)
,


 
 
 
 
(
3
1
6
,
'
D
e
b
u
g
g
i
n
g
'
)
,


 
 
 
 
(
3
1
7
,
'
V
a
l
i
d
a
t
i
o
n
'
)
,


 
 
 
 
(
3
1
8
,
'
V
e
r
s
i
o
n
i
n
g
'
)
,


 
 
 
 
(
3
1
9
,
'
S
e
c
u
r
i
t
y
'
)
,


 
 
 
 
(
3
2
0
,
'
P
e
r
f
o
r
m
a
n
c
e
'
)
,


 
 
 
 
(
3
2
1
,
'
O
b
s
e
r
v
a
b
i
l
i
t
y
'
)
,


 
 
 
 
(
3
2
2
,
'
E
x
t
e
n
s
i
o
n
'
)
,


 
 
 
 
(
3
2
3
,
'
P
l
u
g
i
n
 
I
n
t
e
g
r
a
t
i
o
n
'
)
,


 
 
 
 
(
3
2
4
,
'
S
t
o
r
a
g
e
'
)
,


 
 
 
 
(
3
2
5
,
'
A
I
'
)
,


 
 
 
 
(
3
2
6
,
'
V
i
s
i
o
n
'
)
,


 
 
 
 
(
3
2
7
,
'
I
P
C
'
)
,


 
 
 
 
(
3
2
8
,
'
S
e
r
i
a
l
i
z
a
t
i
o
n
'
)
,


 
 
 
 
(
3
2
9
,
'
C
o
m
p
a
t
i
b
i
l
i
t
y
'
)
,


 
 
 
 
(
3
3
0
,
'
C
o
m
p
l
i
a
n
c
e
'
)
,


]
:


 
 
 
 
R
E
L
[
_
i
]
 
=
 
_
n




d
e
f
 
m
a
k
e
_
h
e
a
d
e
r
(
n
u
m
,
 
t
i
t
l
e
)
:


 
 
 
 
d
l
 
=
 
N
L
.
j
o
i
n
(
'
 
 
-
 
'
+
d
 
f
o
r
 
d
 
i
n
 
D
E
P
S
)


 
 
 
 
r
l
 
=
 
N
L
.
j
o
i
n
(
'
 
 
-
 
R
F
C
-
%
0
4
d
 
W
o
r
k
f
l
o
w
 
%
s
'
%
(
k
,
v
)
 
f
o
r
 
k
,
v
 
i
n
 
s
o
r
t
e
d
(
R
E
L
.
i
t
e
m
s
(
)
)
)


 
 
 
 
h
 
=
 
[


 
 
 
 
 
 
 
 
'
#
 
R
F
C
-
%
0
4
d
:
 
%
s
'
%
(
n
u
m
,
 
t
i
t
l
e
)
,


 
 
 
 
 
 
 
 
T
Q
,
 
'
#
#
 
H
e
a
d
e
r
'
,


 
 
 
 
 
 
 
 
T
Q
,


 
 
 
 
 
 
 
 
B
T
,


 
 
 
 
 
 
 
 
'
R
F
C
:
 
R
F
C
-
%
0
4
d
'
%
n
u
m
,


 
 
 
 
 
 
 
 
'
T
i
t
l
e
:
 
%
s
'
%
t
i
t
l
e
,


 
 
 
 
 
 
 
 
'
S
t
a
t
u
s
:
 
P
r
o
p
o
s
e
d
'
,


 
 
 
 
 
 
 
 
'
V
e
r
s
i
o
n
:
 
1
.
0
.
0
'
,


 
 
 
 
 
 
 
 
'
A
u
t
h
o
r
:
 
A
t
l
a
s
 
S
p
e
c
i
f
i
c
a
t
i
o
n
 
C
o
m
m
i
t
t
e
e
'
,


 
 
 
 
 
 
 
 
'
C
r
e
a
t
e
d
:
 
2
0
2
6
-
0
7
-
0
1
'
,


 
 
 
 
 
 
 
 
'
D
e
p
e
n
d
s
 
O
n
:
'
,


 
 
 
 
 
 
 
 
d
l
,


 
 
 
 
 
 
 
 
'
S
u
p
e
r
s
e
d
e
s
:
 
N
o
n
e
'
,


 
 
 
 
 
 
 
 
'
S
u
p
e
r
s
e
d
e
d
 
B
y
:
 
N
o
n
e
'
,


 
 
 
 
 
 
 
 
'
C
a
t
e
g
o
r
y
:
 
W
o
r
k
f
l
o
w
'
,


 
 
 
 
 
 
 
 
'
L
a
y
e
r
:
 
S
t
a
n
d
a
r
d
'
,


 
 
 
 
 
 
 
 
'
N
o
r
m
a
t
i
v
e
:
 
Y
E
S
'
,


 
 
 
 
 
 
 
 
'
A
u
d
i
e
n
c
e
:
 
A
l
l
 
S
u
b
s
y
s
t
e
m
 
T
e
a
m
s
'
,


 
 
 
 
 
 
 
 
'
A
D
R
 
R
e
f
e
r
e
n
c
e
s
:
'
,


 
 
 
 
 
 
 
 
'
 
 
-
 
A
D
R
-
0
0
1
2
'
,


 
 
 
 
 
 
 
 
'
C
o
n
s
t
i
t
u
t
i
o
n
 
R
e
f
e
r
e
n
c
e
s
:
'
,


 
 
 
 
 
 
 
 
'
 
 
-
 
S
e
c
t
i
o
n
 
1
 
(
W
o
r
k
f
l
o
w
 
P
h
i
l
o
s
o
p
h
y
)
'
,


 
 
 
 
 
 
 
 
'
R
e
l
a
t
e
d
 
R
F
C
s
:
'
,


 
 
 
 
 
 
 
 
r
l
,


 
 
 
 
 
 
 
 
'
T
a
r
g
e
t
 
R
e
l
e
a
s
e
:
 
1
.
0
.
0
'
,


 
 
 
 
 
 
 
 
'
R
e
v
i
e
w
 
C
y
c
l
e
:
 
S
p
e
c
i
f
i
c
a
t
i
o
n
 
C
o
m
m
i
t
t
e
e
'
,


 
 
 
 
 
 
 
 
'
C
o
m
p
a
t
i
b
i
l
i
t
y
:
 
C
o
m
p
a
t
i
b
l
e
 
w
i
t
h
 
S
p
e
c
 
1
.
x
'
,


 
 
 
 
 
 
 
 
'
L
a
s
t
 
U
p
d
a
t
e
d
:
 
2
0
2
6
-
0
7
-
0
1
'
,


 
 
 
 
 
 
 
 
B
T
,


 
 
 
 
 
 
 
 
T
Q
,


 
 
 
 
]


 
 
 
 
r
e
t
u
r
n
 
N
L
.
j
o
i
n
(
h
)
 
+
 
N
L




d
e
f
 
w
f
(
n
a
m
e
,
 
c
o
n
t
e
n
t
)
:


 
 
 
 
p
a
t
h
 
=
 
o
s
.
p
a
t
h
.
j
o
i
n
(
D
I
R
,
 
n
a
m
e
)


 
 
 
 
w
i
t
h
 
o
p
e
n
(
p
a
t
h
,
 
'
w
'
,
 
e
n
c
o
d
i
n
g
=
'
u
t
f
-
8
'
)
 
a
s
 
f
:


 
 
 
 
 
 
 
 
f
.
w
r
i
t
e
(
c
o
n
t
e
n
t
)


 
 
 
 
p
r
i
n
t
(
'
W
r
o
t
e
 
'
 
+
 
n
a
m
e
 
+
 
'
:
 
'
 
+
 
s
t
r
(
o
s
.
p
a
t
h
.
g
e
t
s
i
z
e
(
p
a
t
h
)
)
)




d
e
f
 
t
b
l
(
h
e
a
d
e
r
s
,
 
r
o
w
s
)
:


 
 
 
 
r
 
=
 
[
]


 
 
 
 
r
.
a
p
p
e
n
d
(
'
|
 
'
 
+
 
'
 
|
 
'
.
j
o
i
n
(
h
e
a
d
e
r
s
)
 
+
 
'
 
|
'
)


 
 
 
 
r
.
a
p
p
e
n
d
(
'
|
 
'
 
+
 
'
 
|
 
'
.
j
o
i
n
(
'
-
-
-
'
 
f
o
r
 
_
 
i
n
 
h
e
a
d
e
r
s
)
 
+
 
'
 
|
'
)


 
 
 
 
f
o
r
 
r
o
w
 
i
n
 
r
o
w
s
:


 
 
 
 
 
 
 
 
r
.
a
p
p
e
n
d
(
'
|
 
'
 
+
 
'
 
|
 
'
.
j
o
i
n
(
s
t
r
(
c
)
 
f
o
r
 
c
 
i
n
 
r
o
w
)
 
+
 
'
 
|
'
)


 
 
 
 
r
e
t
u
r
n
 
N
L
.
j
o
i
n
(
r
)




d
e
f
 
m
e
r
m
a
i
d
(
d
)
:


 
 
 
 
r
e
t
u
r
n
 
B
T
 
+
 
N
L
 
+
 
d
 
+
 
N
L
 
+
 
B
T


