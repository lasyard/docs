# TPC-H

<https://www.tpc.org/>

## Build from sources

:::{include} /_files/frags/toolchain/ubuntu_gcc_11.txt
:::

Enter the source directory:

```console
$ cd TPC-H\ V3.0.1/
```

Create makefile:

```console
$ cd dbgen/
$ cp makefile.suite Makefile
```

Edit the `Makefile`:

:::{literalinclude} /_files/ubuntu/workspace/tpc_h/dbgen/Makefile
:diff: /_files/ubuntu/workspace/tpc_h/dbgen/makefile.suite
:::

Build:

```console
$ make -j
```

After building, executables `dbgen`, `qgen` are created:

```console
$ ls *gen
dbgen  qgen
```

## Usage

### dbgen

Use `dbgen` to generate data:

```console
$ ./dbgen -vf -s 0.01 -T L
TPC-H Population Generator (Version 3.0.0)
Copyright Transaction Processing Performance Council 1994 - 2010
Generating data for lineitem table/
Preloading text ... 100%
done.
```

Explain the parameters:

- `-s`: Scale of the database population. Scale 1.0 represents ~1 GB of data
- `-T`: Generate the data for a particular table only. `L` stands for table lineitem

The command will produce a CSV file named `lineitem.tbl`. The separator is `|`. The separator at the end of line is redundency, remove it:

```console
$ sed -i -e 's/|$//g' *.tbl
```

### qgen

Generate query statements, and redirect the output to file `tpc_h_query.sql`:

```console
$ DSS_QUERY=queries/ ./qgen -v -s 0.01 >tpc_h_query.sql
```

The output SQL statments:

:::{literalinclude} /_files/ubuntu/workspace/tpc_h/tpc_h_query.sql
:::
