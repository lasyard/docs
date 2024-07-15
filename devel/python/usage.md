# Python Usage

## Create venv

```sh
python3 -m venv .venv
```

Activate the venv:

```sh
. .venv/bin/activate
```

A very old `pip3` is installed in this venv, so upgrade it first:

```sh
pip install --upgrade pip
```

:::{tip}
This `pip3` is too old to have a `config` sub-command. You can edit the config file mannually:

```sh
vi .venv/pyvenv.cfg
```

:::{literalinclude} /_files/common/work/venv/pyvenv.cfg
:diff: /_files/common/work/venv/pyvenv.cfg.orig
:class: file-content
:::
:::

You may need to upgrade `virtualenv`, too:

```sh
pip install --upgrade virtualenv
```
