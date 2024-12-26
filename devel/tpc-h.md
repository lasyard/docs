# TPC-H

<https://www.tpc.org/>

## Build from sources

::::{plat} centos
:vers: CentOS 8.5

:::{include} /_files/frags/toolchain/centos_gcc_11.txt
:::

```sh
cd TPC-H\ V3.0.1/
```

Create makefile:

```sh
cd dbgen/
cp makefile.suite Makefile
vi Makefile
```

:::{literalinclude} /_files/centos/work/tpc-h/dbgen/Makefile
:diff: /_files/centos/work/tpc-h/dbgen/makefile.suite
:class: file-content
:::

Build:

```sh
make
```

After building, executables `dbgen`, `qgen` are created.

::::

## Usage

### dbgen

Use `dbgen` to generate data:

```sh
./dbgen -vf -s 0.01 -T L
```

- `-s`: Scale of the database population. Scale 1.0 represents ~1 GB of data
- `-T`: Generate the data for a particular table only. `L` stands for table lineitem

The command will produce a CSV file named `lineitem.tbl`. The separator is `|`. The separator at the end of line is redundency, remove it:

```sh
sed -i -e 's/|$//g' *.tbl
```

### qgen

Generate query statements:

```sh
DSS_QUERY=queries/ ./qgen -v -s 0.01
```

:::{literalinclude} /_files/centos/console/qgen/v_s_0.01.sql
:language: sql
:class: cli-output
:::
