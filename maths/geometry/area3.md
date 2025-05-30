# 面积问题（三）

## 题目

![area3](/_images/maths/geometry/area3.png)

如图所示是一个长方形 $ABCD$, $E$ 为 $AD$ 上一点，$F$ 为 $AB$ 上一点。$\triangle AEF$, $\triangle BCF$, $\triangle CDE$ 的面积分别为 $3$, $4$, $5$. 求 $\triangle CEF$ 的面积。

## 解

用 $a$, $b$, $c$, $d$ 分别表示线段 $AE$, $ED$, $AF$, $FB$ 的长度。

由 $\triangle AEF$ 的面积为 $3$, 可知：

$$
ac = 6
$$ (ar3_1)

由 $\triangle BCF$ 的面积为 $4$, 可知：

$$
(a + b)d = 8
$$ (ar3_2)

由 $\triangle CDE$ 的面积为 $5$, 可知：

$$
(c + d)b = 10
$$ (ar3_3)

{eq}`ar3_2` $+$ {eq}`ar3_3`, 可得：

$$
ad + bc + 2bd = 18
$$ (ar3_4)

{eq}`ar3_2` $\times$ {eq}`ar3_3`, 可得：

$$
(ac)(bd) + (ad + bc)(bd) + (bd)^2 = 80
$$ (ar3_5)

将 {eq}`ar3_4` 两边乘以 $bd$ 再减去 {eq}`ar3_5`, 可得：

$$
(bd)^2 - (ac)(bd) = 18bd - 80
$$ (ar3_6)

将 {eq}`ar3_1` 代入 {eq}`ar3_6` 并化简后得：

$$
(bd)^2 - 24bd + 80 = 0
$$ (ar3_7)

解此以 $bd$ 为元的一元二次方程，可得两个根为 $20$ 和 $4$. 但根据 {eq}`ar3_4`, $bd = 20$ 不合理，只能是 $bd = 4$, 于是：

$$
ad + bc = 18 - 2bd = 10
$$ (ar3_8)

现在求长方形 $ABCD$ 面积，即：

$$
\begin{split}
(a + b)(c + d) &= ac + ad + bc + bd \\
               &= 6 + 10 + 4 \\
               &= 20
\end{split}
$$ (ar3_9)

于是 $\triangle CEF$ 面积为 $20 - 3 - 4 - 5 = 8$.
