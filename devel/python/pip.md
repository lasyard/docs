# pip

<https://pypi.org/project/pip/>

The PyPA recommended tool for installing Python packages.

## Usage

### Show version

```sh
pip3 --version
```

{.cli-output}

```text
pip 24.0 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

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
pip3 install PySocks -i https://pypi.tuna.tsinghua.edu.cn/simple
```

If python is managed by other package manager, for example, `brew` on macOS. Try:

```sh
pip3 install -r requirements.txt --break-system-packages
```
