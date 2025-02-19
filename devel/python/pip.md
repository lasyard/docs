# pip

<https://pypi.org/project/pip/>

## Usage

### Show version

```console
$ pip3 --version
pip 24.0 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

Updagrade pip:

```sh
sudo pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
```

:::{tip}
Command `config set` may not exist for low version of `pip`.
:::

## Set index-url

```sh
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## Install a package

```sh
pip3 install setuptools
```

Install with specified index-url:

```sh
pip3 install python-socks -i https://pypi.tuna.tsinghua.edu.cn/simple
```

If python is managed by other package manager, for example, `brew` on macOS. Try:

```sh
pip3 install -r requirements.txt --break-system-packages
```

Show info of a package:

```sh
pip show datasets
```
