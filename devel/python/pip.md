# Package Installer for Python

<https://pypi.org/project/pip/>

## Show version

```console
$ pip3 --version
pip 24.0 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

## Set index-url

```console
$ pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

:::{tip}
Command `config set` may not exist for low version of `pip`.
:::

## Install packages

```console
$ pip3 install setuptools
```

Install with specified index-url:

```console
$ pip3 install python-socks -i https://pypi.tuna.tsinghua.edu.cn/simple
```

:::{tip}
If python is managed by other package manager, for example, `brew` on macOS. Try:

```console
$ pip3 install -r requirements.txt --break-system-packages
```

:::

## Show info of packages

```console
$ pip show datasets
```

## Upgrade pip

```console
$ sudo pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
```
