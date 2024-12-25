# spack

<https://spack.io/>

## Install

```sh
mkidr ~/opt
cd ~/opt
git clone https://github.com/spack/spack.git
```

```sh
. ~/opt/spack/share/spack/setup-env.sh
```

Check the version:

```console
$ spack -V
0.24.0.dev0 (e9cdcc4af02002f870955f9b1b12422b81f27c05)
```

## Configure

Set environment:

```sh
export SPACK_USER_CACHE_PATH="${HOME}/opt/spack-data"
```

Show configs in section `config`:

```sh
spack config get config
```

:::{literalinclude} /_files/ubuntu/console/spack/config_get_config.txt
:language: yaml
:class: cli-output
:::

Use `curl` to fetch packages:

```sh
spack config add config:url_fetch_method:curl
```

A config file `~/.spack/config.yaml` is generated for the current user, and its contents are merged with the default config as the final configuration.

Change some important paths out of spack installation dir:

```sh
spack config add config:install_tree:root:~/opt/spack-data/tree
spack config add config:license_dir:~/opt/spack-data/licenses
spack config add config:source_cache:~/opt/spack-data/sources
spack config add config:environments_root:~/opt/spack-data/environments
```

## Bootstrap

Show configs in section `bootstrap`:

:::{literalinclude} /_files/ubuntu/console/spack/config_get_bootstrap.txt
:language: console
:::

Check the root dir:

```console
$ spack bootstrap root
/home/xxxx/opt/spack-data/bootstrap
```

This is where the bootstrap softwares are installed.

Check status:

:::{literalinclude} /_files/ubuntu/console/spack/bootstrap_status.txt
:language: console
:::

Run bootstraping:

```sh
spack bootstrap now
```

After bootstraping, check the status again:

:::{literalinclude} /_files/ubuntu/console/spack/bootstrap_status_ok.txt
:language: console
:::

Show packages installed for bootstraping:

:::{literalinclude} /_files/ubuntu/console/spack/b_find.txt
:language: console
:::

## Env

List environments:

```console
$ spack env list
==> No environments
```

Create an environment `default`:

```console
$ spack env create default
==> Created environment default in: /home/jyg/opt/spack-data/environments/default
==> Activate with: spack env activate default
```

List environments again:

```console
$ spack env list
==> 1 environments
    default
```

Check environments status:

```console
$ spack env status
==> No active environment
```

Activate the environment `default`:

```sh
spack env activate default
```

Now check the evironments status again:

```console
$ spack env status
==> In environment default
```

Deactivate the current environment:

```sh
spack env deactivate
```

## Compiler

List available compilers:

```console
$ spack compiler list
==> No compilers available. Run `spack compiler find` to autodetect compilers
```

:::{literalinclude} /_files/ubuntu/console/spack/compiler_find.txt
:language: console
:::

:::{note}
The compiler settings were written to user scope, so they are available for all envs of the user. If the command was run with an active env, then the settings are only available in that env.
:::

Now check the available compilers again:

:::{literalinclude} /_files/ubuntu/console/spack/compiler_list.txt
:language: console
:::

## Install packages

:::{note}
If you moved your spack directory, you need to:

```sh
spack reindex
```

:::

These commands are run with `default` env activated.

Find packages in the current environment:

:::{literalinclude} /_files/ubuntu/console/spack/find_0.txt
:language: console
:::

Search for a package and its versions:

:::{literalinclude} /_files/ubuntu/console/spack/list_gcc.txt
:language: console
:::

Add packages to the current environment:

```console
$ spack add lmod ninja
==> Adding lmod to environment default
==> Adding ninja to environment default
```

Now, redo finding packages:

:::{literalinclude} /_files/ubuntu/console/spack/find_1.txt
:language: console
:::

:::{tip}
You can check the install plan by:

```sh
spack spec -lI
```

:::

Start to install:

```sh
spack install
```

After installed successfully, run `spack find` again:

:::{literalinclude} /_files/ubuntu/console/spack/find_2.txt
:language: console
:::

## modules

Show configs in section `modules`:

:::{literalinclude} /_files/ubuntu/console/spack/config_get_modules.txt
:language: console
:::

Configure modules (use lmod):

```sh
spack config add modules:default:roots:tcl:~/opt/spack-data/modules
spack config add modules:default:roots:lmod:~/opt/spack-data/lmod
spack config add modules:default:enable:lmod
spack config remove modules:default:enable:tcl
```

Generate module files:

```sh
spack module lmod refresh
```

Then the modules can be used:

```sh
ml use ~/opt/spack-data/lmod/linux-ubuntu22.04-x86_64/Core
```

### Anonymous env

```sh
mkdir spack-cache-env
cd spack-cache-env/
```

Create an indenpendent `env` in current directory and activate it:

```sh
spack env create -d .
spack env activate .
```

### Mirror

```sh
mkdir ~/opt/spack-mirror
spack mirror create -d ~/opt/spack-mirror --all
```

### Build Cache

Spack buildcache is almost the same as mirror, but contains only prebuilt binaries.

Add a mirror:

```sh
export TOKEN=xxxxxxxxxxxxxxxx
spack mirror add --unsigned --oci-username lasyard --oci-password-variable TOKEN github oci://ghcr.io/lasyard/spack-built
```

Show mirrors:

```console
$ spack mirror list
github       [sb] oci://ghcr.io/lasyard/spack-built
spack-public [s ] https://mirror.spack.io
```

Push to mirror `github` the prebuilt binaries:

```sh
spack buildcache push --update-index github
```

If `--update-index` is omitted in the above command, you can do:

```sh
spack buildcache update-index github
```

Then you can check the content of the buildcache:

```sh
spack buildcache list
```

In fact, Spack will create the oci image, and put each software to an unique version of the image and tag it by the software name, version and hash.

:::{note}

You must be in an environment to push, also the prebuilt being pushed must be already installed. So you'd better do pushing before `spcak gc`, which will uninstall unnecessary packages.
:::
