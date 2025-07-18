# 对三个小游戏的分析

三个小游戏，规则分别如下：

- **抓棋子**：若干堆棋子，双方轮流从任一堆中抓取任意个棋子，取走最后一个者赢。
- **打木棍**：一排木棍，双方轮流击打，一次可以击倒一根或相邻的两根，击倒最后一根者赢。
- **分硬币**：若干堆硬币，两人轮流将任一堆分为数目不等的两堆，首先不能执行此操作者输。

## 分析

这三个看似不同的游戏其实都有着相同的本质，那就是——异或 (exclusive OR). 所谓异或是一种二进制的位运算。运算的规则是：用二进制表示参与运算的数，如果在某位上有奇数个数是 $1$, 则结果的这一位上就是 $1$, 反之是 $0$.

对于抓棋子，操作者面对的局面可以用一些数的集合来表示，每个数代表一堆棋子的数目。这种表示法同样可以用于分硬币。对于打木棍，我们把挨在一起的木棍视为一“堆”，这种表示法也就可以适用了。

然后我们定义一个映射：$V(x) = n$. $n$ 是这样确定的：

1. 如果一个数 $x$ 代表的局面已无法进行下一步操作，$V(x) = 0$. 比如抓棋子打木棍中 $x = 0$, 分硬币中 $x = 0, 1, 2$
2. $V(\Bbb{X})$ 等于组成局面 $\Bbb{X}$ 的所有数的 $V$ 值的异或
3. 对于所有 $k < n$, 都存在一个由 $x$ 经过一步操作变成的局面 $\Bbb{X}$, 使得 $V(\Bbb{X}) = k$
4. 不存在一个由 $x$ 经过一步操作变成的局面 $\Bbb{X}$, 使得 $V(\Bbb{X}) = n$

注意一个数经过操作以后可能变成不只一个数，例如在打木棍和分硬币中，一堆可以变为两堆。

如果对一个局面，无论对方如何操作，你均有策略使其输掉，则称这种局面为输局。下面我们将证明 $V(\Bbb{X}) = 0$ 的局面 $\Bbb{X}$ 是输局。

首先，设 $\Bbb{X}$ 经过一步操作后变为 $\Bbb{Y}$, 则一定有 $V(\Bbb{Y}) > 0$. 这是因为，游戏规则保证了每次只能对一个数进行操作。根据 $V$ 值定义的第 4 条，没有一个数经过操作之后能保持 $V$ 值不变。再根据异或运算的性质，总的 $V$ 值也一定会变。

然后我们将证明当 $V(\Bbb{X}) > 0$ 时，总存在一个经由一步操作变成的局面 $\Bbb{Y}$, 使得 $V(\Bbb{Y}) = 0$. 此时，我们要在 $\Bbb{X}$ 中寻找一个数 $x$, 使得 $V(\Bbb{X}) \oplus V(x) < V(x)$（$\oplus$ 是表示异或的符号）。这样的 $x$ 总是存在的，这是因为，将 $V(\Bbb{X})$ 和所有数的 $V$ 值写成二进制，设 $V(\Bbb{X})$ 的最高位是第 $i$ 位，检查所有 V 值的第 $i$ 位，必然可以找到至少一个是 $1$ 的，它就是符合要求的数。于是我们操作它使之变为 $\Bbb{Y}$, 满足 $V(\Bbb{Y}) = V(\Bbb{X}) \oplus V(x)$, 这样总的 $V$ 值又变回了 $0$. 这一操作也总是可行的，由定义的第 3 条保证。

此后，不管对方如何操作，你总可以保持 $V = 0$ 一直到对方无法操作。

## 映射关系

那么这个神秘的函数 $V$ 是什么样子呢？

### 抓棋子

对于抓棋子，映射关系很简单，$V(x) = x$.

因为任何一个数都可以经过一步操作变为比它小的任意数，所以它的 $V$ 值就只能等于它本身。

### 打木棍

对于打木棍，一般来说，对于任意非负整数 $k$:

$$
\begin{split}
     V(12k) &= 4 (k \ne 0, V(0) = 0) \\
 V(12k + 1) &= 1 \\
 V(12k + 2) &= 2 \\
 V(12k + 3) &= 8 (k \ne 0, 1, 3, V(3) = 3, V(15) = 7, V(39) = 3) \\
 V(12k + 4) &= 1 (k \ne 2, V(28) = 5) \\
 V(12k + 5) &= 4 \\
 V(12k + 6) &= 7 (k \ne 0, 1, V(6) = 3, V(18) = 3) \\
 V(12k + 7) &= 2 \\
 V(12k + 8) &= 1 \\
 V(12k + 9) &= 8 (k \ne 0, 1, 4, V(9) = 4, V(21) = 4, V(57) = 4) \\
V(12k + 10) &= 2 (k \ne 1, 2, 5, V(22) = 6, V(34) = 6, V(70) = 6) \\
V(12k + 11) &= 7 (k \ne 0, V(11) = 6)
\end{split}
$$

1 - 99 范围内的数映射如下：

:::{list-table}
:header-rows: 1
:align: left

- - 映射值
  - 数
- - $0$
  -
- - $1$
  - $1,  4,  8, 13, 16, 20, 25, 32, 37, 40, 44, 49, 52, 56, 61, 64, 68, 73, 76, 80, 85, 88, 92, 97$
- - $2$
  - $2,  7, 10, 14, 19, 26, 31, 38, 43, 46, 50, 55, 58, 62, 67, 74, 79, 82, 86, 91, 94, 98$
- - $3$
  - $3,  6, 18, 39$
- - $4$
  - $5,  9, 12, 17, 21, 24, 29, 36, 41, 48, 53, 57, 60, 65, 72, 77, 84, 89, 96$
- - $5$
  - $28$
- - $6$
  - $11, 22, 34, 70$
- - $7$
  - $15, 23, 30, 35, 42, 47, 54, 59, 66, 71, 78, 83, 90, 95$
- - $8$
  - $27, 33, 45, 51, 63, 69, 75, 81, 87, 93, 99$

:::

### 分硬币

暂未找到规律。1 - 99 范围内的数映射如下：

:::{list-table}
:header-rows: 1
:align: left

- - 映射值
  - 数
- - $0$
  - $1,  2,  4,  7, 10, 20, 23, 26, 50, 53$
- - $1$
  - $3,  6,  9, 12, 15, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61$
- - $2$
  - $5,  8, 11, 14, 17, 29, 32, 35, 38, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 97$
- - $3$
  - $13, 16, 19, 22, 25, 30, 59, 62, 65, 68, 71, 74, 77, 86, 89, 92, 95, 98$
- - $4$
  - $18, 21, 24, 27, 33, 36, 39, 42, 45, 48, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91, 94$
- - $5$
  - $41, 44, 47, 56, 80, 83, 96, 99$
- - $6$
  -
- - $7$
  - $87, 90, 93$

:::

## 对打木棍游戏中规律的证明

显然，对于任何非 $0$ 数，都可以经一步操作使之 $V$ 值变为 $0$, 只要将其分为相等的两“堆”即可，所以任何非 $0$ 数的 $V$ 值都不等于 $0$.

### $12k$

考虑第一行形如 $12k$ 的数，当 $k \ne 0$, $12k = 12(k - 1) + 7 + 3 + 2$, 而 $V(12(k - 1) + 7) = 2$, $V(3) = 3$, 所以只要击倒两根使之分为数量分别为 $3$ 和 $12(k - 1) + 7$ 的两堆即可使 $V$ 值变为 $2 \oplus 3 = 1$.

同理有：

$$
\begin{split}
12k = 12(k - 1) + 8 + 3 + 1, V(12(k - 1) + 8) \oplus V(3) = 2 \\
12k = 12(k - 1) + 8 + 2 + 2, V(12(k - 1) + 8) \oplus V(2) = 3
\end{split}
$$

存在一步操作使得 $V < 4$.

关键是证明形如 $12k$ 的数不可能经一步操作变成 $V$ 值为 $4$ 的局面。

$4 = 1 \oplus 5 = 2 \oplus 6 = 3 \oplus 7$, 如果操作后的局面的 $V$ 值为 $4$, 则只可能是这三种情况。

$V$ 值为 $1$ 的数除以 $12$ 的余数属于集合 $\set{1, 4, 8}$; $V$ 值为 $5$ 的数除以 $12$ 的余数属于集合 $\set{4}$; 它们加起来以后余数属于集合 $\set{0, 5, 8}$, 而形如 $12k$ 的数经过一步操作后剩下的总数除以 $12$ 的余数应为 $11$ 或 $10$, 因此不可能变成这种局面。

以下的证明沿用相同的方法，为了简洁，只写出数字和公式。

这里面，通过分析除以 $12$ 后的余数排查可能的局面是通用方法，故先将各种可能列出：

|  $V$ | 可能出现的余数                   |
| ---: | -------------------------------- |
|  $1$ | $\set{1, 2, 4, 5, 8, 9, 10}$     |
|  $2$ | $\set{2, 3, 4, 7, 8, 10, 11}$    |
|  $3$ | $\set{0, 2, 3, 4, 6, 8, 10, 11}$ |
|  $4$ | $\set{0, 1, 2, 5, 6, 8, 9}$      |
|  $5$ | $\set{1, 2, 4, 5, 6, 8, 9, 10}$  |
|  $6$ | $\set{0, 2, 3, 4, 7, 10, 11}$    |
|  $7$ | $\set{0, 2, 3, 6, 7, 8, 11}$     |

其详细推理过程见“余数的推理过程”一节。

在 $12k$ 的情况下，一步操作后的余数为 $\set{10, 11}$, 不在 $V = 4$ 时可能的余数集合里。

至此，我们证明了 $V(12k) = 4 (k \ne 0)$ 是正确的。

### $12k + 1$

一步操作后的余数为 $\set{0, 11}$, 不在 $V = 1$ 时可能的余数集合里。

### $12k + 2$

$$
1: 12k + 2 = 12k + 1 + 1, V(12k + 1) = 1
$$

存在一步操作使得 $V < 2$.

一步操作后的余数为 $\set{0, 1}$, 不在 $V = 2$ 时可能的余数集合里。

### $12k + 3$

$$
\begin{split}
1&: 12k + 3 = 12k + 1 + 2, V(12k + 1) = 1 \\
2&: 12k + 3 = 12k + 2 + 1, V(12k + 2) = 2 \\
3&: 12k + 3 = 12(k - 1) + 4 + 10 + 1, V(12(k - 1) + 4) \oplus V(10) = 3, k \ne 0, 3 \\
4&: 12k + 3 = 12(k - 1) + 2 + 11 + 2, V(12(k - 1) + 2) \oplus V(11) = 4, k \ne 0 \\
5&: 12k + 3 = 12(k - 1) + 4 + 9 + 2, V(12(k - 1) + 4) \oplus V(9) = 5, k \ne 0, 3 \\
6&: 12k + 3 = 12k + 2 + 1, V(12k) \oplus V(2) = 6, k \ne 0 \\
7&: 12k + 3 = 12(k - 2) + 4 + 22 + 1, V(12(k - 2) + 4) \oplus V(22) = 7, k \ne 0, 1, 4 \\
7&: 12k + 3 = 51 = 16 + 34 + 1, V(16) \oplus V(34) = 7, k = 4
\end{split}
$$

存在一步操作使得 $V < 8$.

一步操作后的余数为 $\set{1, 2}$, 不在 $V = 8$ 时可能的余数集合（空集）里。

此例中 $k = 0, 1, 3$ 时为例外，需单独验证。

- $k = 0$ 时以上 $1, 2$ 仍成立，显然 $V(3) = 3$
- $k = 1$ 时以上 $1 - 6$ 仍成立，考察 $V = 7$ 时可能的余数集合，出现了 $2$, 进一步排查发现这是不可能的
- $k = 3$ 时以上 $1, 2$ 仍成立，考察 $V = 3$ 时可能的余数集合，出现了 $2$, 进一步排查发现这是不可能的

### $12k + 4$

一步操作后的余数为 $\set{2, 3}$, 考察 $V = 1$ 时可能的余数集合，出现了 $2$, 这只能由 $28 = 11 + 15 + 2$ 造成，需要单独验证：

$$
\begin{split}
1&: 28 = 11 + 15 + 2, V(11) \oplus V(15) = 1 \\
2&: 28 = 22 + 5 + 1, V(22) \oplus V(5) = 2 \\
3&: 28 = 26 + 1 + 1, V(26) \oplus V(1) = 3 \\
4&: 28 = 23 + 3 + 2, V(23) \oplus V(3) = 4
\end{split}
$$

存在一步操作使得 $V < 5$.

考察 $V = 5$ 时可能的余数集合，出现了 $2$, 进一步排查发现这是不可能的。

### $12k + 5$

$$
\begin{split}
1&: 12k + 5 = 12k + 4 + 1, V(12k + 4) = 1, k \ne 2 \\
1&: 12k + 5 = 29 = 10 + 18 + 1, V(10) \oplus V(18) = 1, k = 2 \\
2&: 12k + 5 = 12k + 1 + 3 + 1, V(12k + 1) \oplus V(3) = 2 \\
3&: 12k + 5 = 12k + 1 + 2 + 2, V(12k + 1) \oplus V(2) = 3
\end{split}
$$

存在一步操作使得 $V < 4$.

一步操作后的余数为 $\set{3, 4}$, 不在 $V = 4$ 时可能的余数集合里。

### $12k + 6$

$$
\begin{split}
1&: 12k + 6 = 12k + 2 + 3 + 1, V(12k + 2) \oplus V(3) = 1 \\
2&: 12k + 6 = 12k + 1 + 3 + 2, V(12k + 1) \oplus V(3) = 2 \\
3&: 12k + 6 = 12(k - 1) + 11 + 5 + 2, V(12(k - 1) + 11) \oplus V(5) = 3, k \ne 0, 1 \\
4&: 12k + 6 = 12k + 5 + 1, V(12k + 5) = 4 \\
5&: 12k + 6 = 12k + 4 + 2, V(12k) \oplus V(4) = 5, k \ne 0 \\
6&: 12k + 6 = 12(k - 1) + 1 + 15 + 2, V(12(k - 1) + 1) \oplus V(15) = 6, k \ne 0
\end{split}
$$

存在一步操作使得 $V < 7$.

一步操作后的余数为 $\set{4, 5}$, 不在 $V = 7$ 时可能的余数集合里。

此例中 $k = 0, 1$ 时为例外，需单独验证。首先以上 $1, 2$ 仍成立，考察 $V = 3$ 时可能的余数集合，出现了 $4$, 进一步排查发现这是不可能的。

### $12k + 7$

$$
\begin{split}
1&: 12k + 7 = 12k + 2 + 3 + 2, V(12k + 2) \oplus V(3) = 1
\end{split}
$$

存在一步操作使得 $V < 2$.

一步操作后的余数为 $\set{5, 6}$, 不在 $V = 2$ 时可能的余数集合里。

### $12k + 8$

一步操作后的余数为 $\set{6, 7}$, 不在 $V = 1$ 时可能的余数集合里。

### $12k + 9$

$$
\begin{split}
1&: 12k + 9 = 12k + 8 + 1, V(12k + 8) = 1 \\
2&: 12k + 9 = 12k + 7 + 2, V(12k + 7) = 2 \\
3&: 12k + 9 = 12k + 7 + 1 + 1, V(12k + 7) \oplus V(1) = 3 \\
4&: 12k + 9 = 12(k - 2) + 4 + 28 + 1, V(12(k - 2) + 4) \oplus V(28) = 4, k \ne 0, 1, 4 \\
5&: 12k + 9 = 12(k - 1) + 8 + 12 + 1, V(12(k - 1) + 8) \oplus V(12) = 5, k \ne 0 \\
6&: 12k + 9 = 12(k - 1) + 7 + 12 + 2, V(12(k - 1) + 7) \oplus V(12) = 6, k \ne 0 \\
7&: 12k + 9 = 12k + 5 + 3 + 1, V(12k + 5) \oplus V(3) = 7
\end{split}
$$

存在一步操作使得 $V < 8$.

一步操作后的余数为 $\set{7, 8}$, 不在 $V = 8$ 时可能的余数集合（空集）里。

此例中 $k = 0, 1, 4$ 时为例外，需单独验证。首先以上 $1 - 3$ 仍成立，考察 $V = 4$ 时可能的余数集合，出现了 $8$, 进一步排查发现这是不可能的。

### $12k + 10$

$$
\begin{split}
1&: 12k + 10 = 12k + 8 + 2, V(12k + 8) = 1
\end{split}
$$

存在一步操作使得 $V < 2$.

一步操作后的余数为 $\set{8, 9}$, 考察 $V = 2$ 时可能的余数集合，出现了 $8$, 这只能是以下三种情况：

- $22 = 11 + 9 + 2, V(11) \oplus V(9) = 2$
- $34 = 11 + 21 + 2, V(11) \oplus V(21) = 2$
- $70 = 11 + 57 + 2, V(11) \oplus V(57) = 2$

这三种情况下均有：

$$
\begin{split}
3&: 12k + 10 = 12k + 7 + 1 + 2, V(12k + 7) \oplus V(1) = 3 \\
4&: 12k + 10 = 12k + 6 + 3 + 1, V(12K + 6) \oplus V(3) = 4, k \ne 0, 1 \\
4&: 12k + 10 = 22 = 15 + 6 + 1, V(15) \oplus V(6) = 4, k = 1 \\
5&: 12k + 10 = 12k + 8 + 2, V(12k) \oplus V(8) = 5
\end{split}
$$

一步操作后的余数为 $\set{8, 9}$, 不在 $V = 6$ 时可能的余数集合里。

### $12k + 11$

$$
\begin{split}
1&: 12k + 11 = 12k + 7 + 3 + 1, V(12k + 7) \oplus V(3) = 1 \\
2&: 12k + 11 = 12k + 4 + 6 + 1, V(12k + 4) \oplus V(6) = 2, k \ne 2 \\
2&: 12k + 11 = 35 = 12 + 22 + 1, V(12) \oplus V(22) = 2, k = 2 \\
3&: 12k + 11 = 12k + 8 + 2 + 1, V(12k + 8) \oplus V(2) = 3 \\
4&: 12k + 11 = 12k + 6 + 3 + 2, V(12k + 6) \oplus V(3) = 4, k \ne 0, 1 \\
4&: 12k + 11 = 11 = 9 + 2, V(9) = 4, k = 0 \\
4&: 12k + 11 = 23 = 21 + 2, V(21) = 4, k = 1 \\
5&: 12k + 11 = 12k + 5 + 4 + 2, V(12k + 5) \oplus V(4) = 5 \\
6&: 12k + 11 = 12k + 6 + 4 + 1, V(12k + 6) \oplus V(4) = 6, k \ne 0, 1 \\
6&: 12k + 11 = 23 = 22 + 1, V(22) = 6, k = 1
\end{split}
$$

存在一步操作使得 $V < 6$.

一步操作后的余数为 $\set{9, 10}$, 不在 $V = 7$ 时可能的余数集合里。

此例中 $k = 0$ 时为例外，需单独验证。首先以上 $1 - 5$ 仍成立，考察 $V = 6$ 时可能的余数集合，出现了 $10$, 进一步排查发现这是不可能的。

注意这其实是个数学归纳法，对某个数成立建立在对比它小的所有数都成立的基础上。

证毕。

### 余数的推理过程

在打木棍游戏中，某个数经过一次操作后变为两个数。根据前面总结出的规律，这两个数除以 $12$ 的余数只能是一个或几个值，二者和的余数范围也就可以确定了。

$1 = 2 \oplus 3 = 4 \oplus 5 = 6 \oplus 7$

$$
\begin{alignat}{3}
2& \set{2, 7, 10}&, 3& \set{3, 6}& \implies& \set{1, 4, 5, 8, 10} \\
4& \set{0, 5, 9}&, 5& \set{4}& \implies& \set{1, 4, 9} \\
6& \set{10, 11}&, 7& \set{3, 6, 11}& \implies& \set{1, 2, 4, 5, 9, 10}
\end{alignat} \implies \set{1, 2, 4, 5, 8, 9, 10}
$$

$2 = 1 \oplus 3 = 4 \oplus 6 = 5 \oplus 7$

$$
\begin{alignat}{3}
1& \set{1, 4, 8}&, 3& \set{3, 6}& \implies& \set{4, 7, 10, 11, 2} \\
4& \set{0, 5, 9}&, 6& \set{10, 11}& \implies& \set{3, 4, 7, 8, 10, 11} \\
5& \set{4}&, 7& \set{3, 6, 11}& \implies& \set{3, 7, 10}
\end{alignat} \implies \set{2, 3, 4, 7, 8, 10, 11}
$$

$3 = 1 \oplus 2 = 4 \oplus 7 = 5 \oplus 6$

$$
\begin{alignat}{3}
1& \set{1, 4, 8}&, 2& \set{2, 7, 10}& \implies& \set{2, 3, 6, 8, 10, 11} \\
4& \set{0, 5, 9}&, 7& \set{3, 6, 11}& \implies& \set{0, 3, 4, 6, 8, 11} \\
5& \set{4}&, 6& \set{10, 11}& \implies& \set{2, 3}
\end{alignat} \implies \set{0, 2, 3, 4, 6, 8, 10, 11}
$$

$4 = 1 \oplus 5 = 2 \oplus 6 = 3 \oplus 7$

$$
\begin{alignat}{3}
1& \set{1, 4, 8}&, 5& \set{4}& \implies& \set{0, 5, 8} \\
2& \set{2, 7, 10}&, 6& \set{10, 11}& \implies& \set{0, 1, 5, 6, 8, 9} \\
3& \set{3, 6}&, 7& \set{3, 6, 11}& \implies& \set{0, 2, 5, 6, 9}
\end{alignat} \implies \set{0, 1, 2, 5, 6, 8, 9}
$$

$5 = 1 \oplus 4 = 2 \oplus 7 = 3 \oplus 6$

$$
\begin{alignat}{3}
1& \set{1, 4, 8}&, 4& \set{0, 5, 9}& \implies& \set{1, 4, 5, 6, 8, 9, 10} \\
2& \set{2, 7, 10}&, 7& \set{3, 6, 11}& \implies& \set{1, 4, 5, 6, 8, 9, 10} \\
3& \set{3, 6}&, 6& \set{10, 11}& \implies& \set{1, 2, 4, 5}
\end{alignat} \implies \set{1, 2, 4, 5, 6, 8, 9, 10}
$$

$6 = 1 \oplus 7 = 2 \oplus 4 = 3 \oplus 5$

$$
\begin{alignat}{3}
1& \set{1, 4, 8}&, 7& \set{3, 6, 11}& \implies& \set{0, 2, 3, 4, 7, 10, 11} \\
2& \set{2, 7, 10}&, 4& \set{0, 5, 9}& \implies& \set{0, 2, 3, 4, 7, 10, 11} \\
3& \set{3, 6}&, 5& \set{4}& \implies& \set{7, 10}
\end{alignat} \implies \set{0, 2, 3, 4, 7, 10, 11}
$$

$7 = 1 \oplus 6 = 2 \oplus 5 = 3 \oplus 4$

$$
\begin{alignat}{3}
1& \set{1, 4, 8}&, 6& \set{10, 11}& \implies& \set{0, 2, 3, 6, 7, 11} \\
2& \set{2, 7, 10}&, 5& \set{4}& \implies& \set{2, 6, 11} \\
3& \set{3, 6}&, 4& \set{0, 5, 9}& \implies& \set{0, 3, 6, 8, 11}
\end{alignat} \implies \set{0, 2, 3, 6, 7, 8, 11}
$$

:::{seealso}
[C++ Code](https://github.com/lasyard/coding-cpp-cmake/blob/main/quiz/games_solution.cpp)
:::
