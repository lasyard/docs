# miniconda

## Install

::::{plat} linux
:vers: CentOS 8.5

Download install scripts:

```sh
wget https://repo.anaconda.com/miniconda/Miniconda3-py310_24.7.1-0-Linux-x86_64.sh
```

Install:

```sh
chmod +x Miniconda3-py310_24.7.1-0-Linux-x86_64.sh
./Miniconda3-py310_24.7.1-0-Linux-x86_64.sh
```

Show the version:

```sh
conda -V
```

{.cli-output}

```text
conda 24.7.1
```

Show info about conda:

```sh
conda info
```

:::{literalinclude} /_files/centos/output/conda/info.txt
:language: text
:class: cli-output
:::

::::
