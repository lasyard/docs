# 面积问题（二）

## 题目

![area2](/_images/maths/geometry/area2.png)

如图所示，$E$ 为长方形 $ABCD$ 外一点，$BE$, $CE$ 分别交 $AD$ 于点 $F$, $G$, $\triangle ABF$, $\triangle CDG$, $\triangle EFG$ 面积分别为 $19$, $8$, $12$, 求长方形 $ABCD$ 面积。

## 解

过 $E$ 作 $AD$ 的垂线落于点 $H$.

$$
\triangle ABF \sim \triangle HEF \implies \frac {AF} {AB} = \frac {FH} {EH}
$$ (ar2_1)

$$
\triangle CDG \sim \triangle EHG \implies \frac {DG} {CD} = \frac {HG} {EH}
$$ (ar2_2)

{eq}`ar2_1` + {eq}`ar2_2`, 得：

$$
\frac {AF} {AB} + \frac {DG} {CD} = \frac {FH} {EH} + \frac {HG} {EH}
$$ (ar2_3)

也就是：

$$
\frac {AF + DG} {AB} = \frac {FG} {EH}
$$ (ar2_4)

根据所给面积，有：

$$
\begin{split}
(AF + DG) \cdot {AB} &= (19 + 8) \cdot 2 \\
FG \cdot {EH} &= 12 \cdot 2
\end{split}
$$ (ar2_5)

将 {eq}`ar2_5` 两个式子代入 {eq}`ar2_4`, 可得：

$$
\frac {(AF + DG)^2} {27} = \frac {FG^2} {12}
$$ (ar2_6)

可解得：

$$
FG = \frac 2 3 (AF + DG)
$$ (ar2_7)

于是长方形 $ABCD$ 面积为：

$$
\begin{split}
(AF + FG + GD) \cdot AB
&= (1 + \frac 2 3)(AF + GD) \cdot AB \\
&= 90
\end{split}
$$ (ar2_8)
