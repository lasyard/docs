# 摄影景深计算

本文用几何光学推导摄影时景深的公式。如下图所示，其中左边粗实线代表镜头的孔径，右边粗实线代表底片。

![photography.png](/_images/physics/photography.png)

设镜头焦距为 $f$, 对焦距离（物距）为 $u$, 像距为 $v$, 底片放在像平面上，由高斯公式：

$$
\frac 1 u + \frac 1 v = \frac 1 f
$$ (1)

可得：

$$
v = \frac {fu} {u - f}
$$ (2)

现在要研究物距为 $u'$ 处的点在底片上的弥散圆直径，同理有：

$$
v' = \frac {fu'} {u' - f}
$$ (3)

所以：

$$
\begin{split}
v' - v  &= \frac {fu'} {u' - f} - \frac {fu} {u - f} \\
        &= \frac {f^2(u - u')} {(u' - f)(u - f)}
\end{split}
$$ (4)

令：

$$
\Delta u = \lvert u' - u \rvert \\
\Delta v = \lvert v' - v \rvert
$$ (5)

于是 {eq}`4`式可写为：

$$
\Delta v = \frac {f^2\Delta u} {(u' - f)(u - f)}
$$ (6)

设镜头光阑（光圈）直径为 $D$, 弥散圆直径为 $d$, 由图示几何关系易得：

$$
\frac D {v'} = \frac d {\Delta v}
$$ (7)

由 {eq}`7`, {eq}`3`, {eq}`6` 可得：

$$
\begin{split}
d &= \frac D {v'} \Delta v \\
  &= \frac {D(u' -f )} {fu'} \frac {f^2\Delta u} {(u' - f)(u - f)} \\
  &= \frac {Df\Delta u} {u'(u - f)} \\
  &= \frac {Df\Delta u} {(u \mp \Delta u)(u - f)}
\end{split}
$$ (8)

当 $d$ 小于最大允许直径 $\phi$, 也就是：

$$
\frac {Df\Delta u} {(u \mp \Delta u)(u - f)} \le \phi
$$ (9)

这时候图像被认为是清晰的，所对应的物距的范围就是景深。(8) 式中负号对应前景深，正号对应后景深。可解得：

$$
\Delta u \le \frac {u(u - f)\phi} {Df \pm (u - f)\phi}
$$ (10)

$\Delta u$ 的允许范围即景深，正号对应前景深，负号对应后景深。注意用该式计算后景深仅在右边分母大于 $0$ 时有效。当分母为 $0$ 时，后景深无穷大，此时的对焦距离即所谓超焦距。

由此很容易得出以下结论：

1. 物距越大，景深越大
2. 焦距越长，景深越小
3. 光圈直径越大，景深越小

以上结论有个前提，即最大允许弥散圆直径是相同的。在底片大小不同时，所允许的最大弥散圆直径也应该不同。我们可以认为该直径与底片宽度成正比，不妨设：

$$
\phi = \varepsilon L
$$ (11)

其中 $L$ 代表底片宽度。另外由图中几何关系易得：

$$
L = 2v\tan\theta
$$ (12)

式中 $\theta$ 为视角的一半，于是：

$$
\phi = \frac {2\varepsilon fu\tan\theta} {u - f}
$$ (13)

得：

$$
\Delta u \le \frac {2\varepsilon u^2 \tan\theta} {D \pm 2\varepsilon u \tan\theta}
$$ (14)

该式表明在视角相同，物距相同的情况下，景深决定于光圈直径。对于小画幅的数码相机来说，焦距短，因而即使 F 数较大，光圈直径依然很小，因此导致景深大。
