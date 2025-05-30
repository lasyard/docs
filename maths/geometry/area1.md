# 面积问题（一）

## 题目

![area1](/_images/maths/geometry/area1.png)

如图所示，一个 $\triangle ABC$, $D$ 在 $BC$ 上，$E$ 在 $CA$ 上，$F$ 在 $AB$ 上，$AD$, $BE$, $CF$ 交于点 $O$. 已知 $\triangle FOA$ 的面积为 $84$, $\triangle DOB$ 的面积为 $40$, $\triangle COD$ 的面积为 $30$, $\triangle EOC$ 的面积为 $35$, 求 $\triangle ABC$ 的面积。

## 解

设 $\triangle BOF$ 的面积为 $x$, $\triangle AOE$ 的面积为 $y$.

$\because \triangle DOB \text{ 与 } \triangle COD \text{ 等高，}\therefore$

$$
\frac {BD} {DC} = \frac {40} {30} = \frac 4 3
$$ (ar1_1)

$\because \triangle ABD \text{ 与 } \triangle ADC \text{ 等高，}\therefore$

$$
\frac {84 + x + 40} {y + 35 + 30} = \frac {DB} {DC} = \frac 4 3
$$ (ar1_2)

$\because \triangle COB \text{ 与 } \triangle EOC \text{ 等高，}\therefore$

$$
\frac {BO} {OE} = \frac {40 + 30} {35} = 2
$$ (ar1_3)

$\because \triangle BOA \text{ 与 } \triangle AOE \text{ 等高，}\therefore$

$$
\frac {84 + x} y = \frac {BO} {OE} = 2
$$ (ar1_4)

由 {eq}`ar1_2`, {eq}`ar1_4` 可解得 $x = 56$, $y = 70$.

答案：$\triangle ABC \text{ 的面积} = 84 + x + 40 + 30 + 35 + y = 315$.

提示：实际上 $\triangle FOA$ 的面积是不需要的，因为可以将 $\triangle BOA$ 的面积整体作为一个未知数处理。
