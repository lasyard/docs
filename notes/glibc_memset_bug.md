# glibc-2.3.5 for ARM 的 memset 函数 bug

函数原型：

```c
void *memset(void *s, int c, size_t n);
```

当 `n < 8` 时功能正常。

当 `n >= 8` 时，实际填充到内存中的字节不再一致，作如下分布：

```c
s[4*i+0] = (char)c;
s[4*i+1] = (char)c | (char)(c >> 8);
s[4*i+2] = (char)c | (char)(c >> 8) | (char)(c >> 16);
s[4*i+3] = (char)c | (char)(c >> 8) | (char)(c >> 16) | (char)(c >> 24);
```

可能会导致如下的错误：

```c
memset(buf, '\xf0', 8);
```

预想的 buf 中的数据：

```text
f0, f0, f0, f0, f0, f0, f0, f0
```

实际上，由于 `'\xf0'` 转为 `int` 型后为 `0xfffffff0`, 数据为：

```text
f0, ff, ff, ff, f0, ff, ff, ff
```
