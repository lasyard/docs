# TPC-H

<https://www.tpc.org/>

The TPC is a non-profit corporation focused on developing data-centric benchmark standards and disseminating objective, verifiable data to the industry.

## 编译源码

::::{plat} centos
编译所用工具链：

- gcc 11.2.1
- GNU Make 4.3

从官网下载源码并解压。

进入解压后的目录：

```sh
cd TPC-H\ V3.0.1/
```

创建 Makefile:

```sh
cd dbgen/
cp makefile.suite Makefile
vi Makefile
```

:::{literalinclude} /_files/centos/work/tpc-h/Makefile
:diff: /_files/centos/work/tpc-h/makefile.suite
:class: file-content
:::

编译：

```sh
make
```

编译以后生成可执行文件 `dbgen`, `qgen`.

::::

## 用法

### dbgen

dbgen 用于生成数据：

```sh
./dbgen -vf -s 0.01 -T L
```

- `-s` 参数设置规模因子，默认为 `1`, 表示生成 1GB 数据
- `-T L` 表示只生成 lineitem 表的数据，如果不指定则生成所有表数据

生成 CSV 格式的数据，文件名为 `lineitem.tbl`, 分隔符为 `|`, 每行末尾的分隔符可能多余，先去掉：

```sh
sed -i -e 's/|$//g' *.tbl
```

### qgen

生成查询语句：

```sh
DSS_QUERY=queries/ ./qgen -v -s 0.01
```

:::{literalinclude} /_files/centos/output/qgen/v_s_0.01.sql
:language: sql
:class: cli-output
:::
