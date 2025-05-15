# Python venv

Create a `venv` in directory `.venv`

```console
$ python -m venv .venv
```

Activate the venv:

```console
$ . .venv/bin/activate
```

Set site configurations:

```console
$ pip config set --site global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
Writing to /home/ubuntu/.venv/pip.conf
```

:::{caution}
Do not forget `--site`, or the user config file would be modified if there is not the site config file. Check the config files by:

```console
$ pip config debug
env_var:
env:
global:
  /etc/xdg/pip/pip.conf, exists: False
  /etc/pip.conf, exists: False
site:
  /home/ubuntu/.venv/pip.conf, exists: True
    global.index-url: https://pypi.tuna.tsinghua.edu.cn/simple
user:
  /home/ubuntu/.pip/pip.conf, exists: False
  /home/ubuntu/.config/pip/pip.conf, exists: True
```

:::
