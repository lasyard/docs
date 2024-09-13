# spack

<https://spack.io/>

A flexible package manager supporting multiple versions, configurations, platforms, and compilers.

## Install

```sh
mkidr ~/opt
cd ~/opt
git clone https://github.com/spack/spack.git
```

```sh
. ~/opt/spack/share/spack/setup-env.sh
```

Show the version:

```sh
spack -V
```

{.cli-output}

```sh
0.22.1
```

## Bootstrap

Show configs in section `bootstrap`:

```sh
spack config get bootstrap
```

:::{literalinclude} /_files/ubuntu/output/spack/config_get_bootstrap.yaml
:language: yaml
:class: cli-output
:::

Change bootstrap root dir:

```sh
spack config add bootstrap:root:~/opt/software/spack/bootstrap
```

A config file `~/.spack/bootstrap.yaml` is generated for the current user, and its contents are merged with the default config as the final configuration.

Check the root dir:

```sh
spack bootstrap root
```

{.cli-output}

```text
/home/xxxx/opt/software/spack/bootstrap
```

This is where the bootstrap softwares are installed.

Check status:

```sh
spack bootstrap status
```

:::{literalinclude} /_files/ubuntu/output/spack/bootstrap_status.txt
:language: text
:class: cli-output
:::

Run bootstraping:

```sh
spack bootstrap now
```

After bootstraping, check the status again:

```sh
spack bootstrap status
```

:::{literalinclude} /_files/ubuntu/output/spack/bootstrap_status_pass.txt
:language: text
:class: cli-output
:::

Show packages installed for bootstraping:

```sh
spack -b find
```

:::{literalinclude} /_files/ubuntu/output/spack/b_find.txt
:language: text
:class: cli-output
:::

## Configure

Show configs in section `config`:

```sh
spack config get config
```

:::{literalinclude} /_files/ubuntu/output/spack/config_get_config.yaml
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
spack config add config:install_tree:root:~/opt/software/spack/tree
spack config add config:license_dir:~/opt/software/spack/licenses
spack config add config:source_cache:~/opt/software/spack/sources
spack config add config:environments_root:~/opt/software/spack/environments
```

## Env

List environments:

```sh
spack env list
```

{.cli-output}

```text
==> No environments
```

Create an environment `base`:

```sh
spack env create base
```

:::{literalinclude} /_files/ubuntu/output/spack/env_create.txt
:language: text
:class: cli-output
:::

List environments again:

```sh
spack env list
```

:::{literalinclude} /_files/ubuntu/output/spack/env_list.txt
:language: text
:class: cli-output
:::

Check environments status:

```sh
spack env status
```

{.cli-output}

```text
==> No active environment
```

Activate the environment `base`:

```sh
spack env activate base
```

or:

```sh
spacktivate base
```

Now check the evironments status again:

```sh
spack env status
```

:::{literalinclude} /_files/ubuntu/output/spack/env_status.txt
:language: text
:class: cli-output
:::

Deactivate the current environment:

```sh
spack env deactivate
```

## Compiler

List available compilers:

```sh
spack compiler list
```

{.cli-output}

```text
==> No compilers available. Run `spack compiler find` to autodetect compilers
```

```sh
spack compiler find
```

:::{literalinclude} /_files/ubuntu/output/spack/compiler_find.txt
:language: text
:class: cli-output
:::

Now check the available compilers again:

```sh
spack compiler list
```

:::{literalinclude} /_files/ubuntu/output/spack/compiler_list.txt
:language: text
:class: cli-output
:::

## Install packages

:::{note}
If you moved your spack directory, you need to:

```sh
spack reindex
```

:::

Find packages in the current environment:

```sh
spack find
```

:::{literalinclude} /_files/ubuntu/output/spack/find_0.txt
:language: text
:class: cli-output
:::

Search for packages:

```sh
spack list gcc
```

:::{literalinclude} /_files/ubuntu/output/spack/list_gcc.txt
:language: text
:class: cli-output
:::

List versions of package `gcc`:

```sh
spack versions gcc
```

:::{literalinclude} /_files/ubuntu/output/spack/versions_gcc.txt
:language: text
:class: cli-output
:::

Add packages to the current environment:

```sh
spack add gcc
```

{.cli-output}

```sh
==> Adding gcc to environment base
```

Now, redo finding packages:

```sh
spack find
```

:::{literalinclude} /_files/ubuntu/output/spack/find_1.txt
:language: text
:class: cli-output
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

## modules

Configure the dir to put module files:

```sh
spack config add modules:default:roots:lmod:~/opt/software/spack/modules
spack config add modules:default:roots:tcl:~/opt/software/spack/modules
spack config add modules:default:enable:lmod
spack config remove modules:default:enable:tcl
```

These configs will be put in `spack.yaml` of the current environment.

Generate module files:

```sh
spack module lmod refresh
```

Then the modules can be used:

```sh
module use ~/opt/software/spack/modules/linux-ubuntu22.04-x86_64/Core
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
mkdir ~/workspace/spack-mirror
spack mirror create -d ~/workspace/spack-mirror --all
```
