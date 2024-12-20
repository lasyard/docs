# Python venv

Create a `venv` in directory `.venv`

```sh
python3 -m venv .venv
```

Activate the venv:

```sh
. .venv/bin/activate
```

::::{tip}
If the `pip3` in the new env is too old to have a `config` sub-command. You can edit the config file mannually:

```sh
vi .venv/pyvenv.cfg
```

:::{literalinclude} /_files/centos/work/venv/pyvenv.cfg
:diff: /_files/centos/work/venv/pyvenv.cfg.orig
:class: file-content
:::
::::

You may need to upgrade `virtualenv`:

```sh
pip install --upgrade virtualenv
```
