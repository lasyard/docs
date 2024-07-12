# TPC-H

<https://www.tpc.org/>

The TPC is a non-profit corporation focused on developing data-centric benchmark standards and disseminating objective, verifiable data to the industry.

{{ for_centos }}

## Build form sources

Download sources from the official website, unzip it.

```sh
cd TPC-H\ V3.0.1/
```

```sh
cd dbgen/
cp makefile.suite Makefile
vi Makefile
```

:::{literalinclude} /_files/common/work/tpc-h/Makefile
:diff: /_files/common/work/tpc-h/makefile.suite
:class: file-content
:::

编译以后生成可执行文件 dbgen, qgen.

## Usage

### dbgen

dbgen 用于生成数据：

```sh
./dbgen -vf -s 0.01 -T L
```

* `-s` 参数设置规模因子，默认为 `1`, 表示生成 1GB 数据
* `-T L` 表示只生成 lineitem 表的数据，如果不指定则生成所有表数据

生成 CSV 格式的数据，文件名为 `lineitem.tbl`, 分隔符为 `|`, 每行末尾的分隔符可能多余，先去掉：

```sh
sed -i -e 's/|$//g' *.tbl
```

### qgen

生成查询语句：

```sh
DSS_QUERY=queries/ ./qgen -v -s 0.01
```

:::{literalinclude} /_files/common/output/tpc-h/tpc-h.sql
:language: sql
:class: file-content
:::
