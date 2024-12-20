# miniconda

<https://www.anaconda.com/>

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

Check the version:

```console
$ conda -V
conda 24.7.1
```

Show info about conda:

:::{literalinclude} /_files/centos/console/conda/info.txt
:language: console
:::

::::
