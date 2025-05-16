# Spack

<https://spack.io/>

## Install

Install just by cloning it:

```console
$ mkidr ~/opt
$ cd ~/opt
$ git clone -c feature.manyFiles=true --depth=2 https://github.com/spack/spack.git
```

Setup environments:

```console
$ . ~/opt/spack/share/spack/setup-env.sh
```

It is OK now! Check the version:

```console
$ spack -V
1.0.0.dev0 (f1ba23316bbea289f6da8d602eeca459c4e79853)
```

## Configure

Set environment:

```sh
export SPACK_USER_CACHE_PATH="${HOME}/opt/spack-data"
```

Show configs in section `config`:

```console
$ spack config get config
```

Now it shows the default configurations in YAML format. Let's make some changes.

Use `curl` to fetch packages (for `curl` supports proxy):

```console
$ spack config add config:url_fetch_method:curl
```

A config file `~/.spack/config.yaml` is generated for the current user, and its contents are merged with the default configurations.

Change some important paths out of spack installation directory:

```console
$ spack config add config:install_tree:root:~/opt/spack-data/tree
$ spack config add config:license_dir:~/opt/spack-data/licenses
$ spack config add config:source_cache:~/opt/spack-data/sources
$ spack config add config:environments_root:~/opt/spack-data/environments
```

## Bootstrap

Show configs in section `bootstrap`:

```console
$ spack config get bootstrap
```

Check the root directory:

```console
$ spack bootstrap root
/home/ubuntu/opt/spack-data/bootstrap
```

This is where the bootstrap softwares are installed.

Check status:

```console
$ spack bootstrap status
Spack v1.0.0.dev0 - python@3.10

[FAIL] Core Functionalities
  [B] MISSING "clingo": required to concretize specs

[FAIL] Binary packages
  [B] MISSING "patchelf": required to relocate binaries


Spack will take care of bootstrapping any missing dependency marked as [B]. Dependencies marked as [-] are instead required to be found on the system.
```

Run bootstraping:

```console
$ spack bootstrap now
```

After bootstraping, check the status again:

```console
$ spack bootstrap status
Spack v1.0.0.dev0 - python@3.10

[PASS] Core Functionalities

[PASS] Binary packages
```

Show packages installed for bootstraping:

```console
$ spack -b find
-- linux-centos7-x86_64 / gcc@10.2.1 ----------------------------
bison@3.0.4  clingo-bootstrap@spack  cmake@3.30.4  gcc-runtime@10.2.1  glibc@2.17  patchelf@0.17.2  python@3.10
==> 7 installed packages
```

## Spack env

List environments:

```console
$ spack env list
==> No environments
```

Create an environment `default`:

```console
$ spack env create default
==> Created environment default in: /home/ubuntu/opt/spack-data/environments/default
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

Activate the environment `default` and check the evironments status again:

```console
$ spack env activate default
$ spack env status
==> In environment default
```

Deactivate the current environment:

```console
$ spack env deactivate
```

You can also create anonymous env at any directory:

```console
$ mkdir senv
$ cd senv/
$ spack env create -d .
==> Created independent environment in: /home/ubuntu/workspace/senv
==> Activate with: spack env activate .
$ spack env activate .
$ spack env status
==> Using spack.yaml in current directory: /home/ubuntu/workspace/senv
```

## Compiler

List available compilers:

```console
$ spack compiler list
==> No compilers available. Run `spack compiler find` to autodetect compilers
```

Detect compilers and list the available compilers again:

```console
$ spack compiler find
==> Added 1 new compiler to /home/ubuntu/.spack/packages.yaml
    gcc@11.4.0
==> Compilers are defined in the following files:
    /home/ubuntu/.spack/packages.yaml
$ spack compiler list
==> Available compilers
-- gcc ubuntu22.04-x86_64 ---------------------------------------
gcc@11.4.0
```

:::{note}
The compiler settings were written to user scope, so they are available for all envs of the user. If the command was run with an active env, then the settings are only available in that env.
:::

## Install packages

:::{note}
If you have moved your spack directory, you need to regenerate the index:

```console
$ spack reindex
==> Created a back-up copy of the DB at /home/ubuntu/opt/spack-data/tree/.spack-db/index.json.bkp
==> The DB at /home/ubuntu/opt/spack-data/tree/.spack-db/index.json has been reindex to v8
```

:::

The following commands are run with `default` env activated.

Find packages in the current environment:

```console
$ spack find
==> In environment default
==> No root specs

==> 0 installed packages
==> 0 concretized packages to be installed (show with `spack find -c`)
```

Search for a package and its versions:

```console
$ spack list ninja
backupninja  generate-ninja  ninja  ninja-fortran  ninja-phylogeny  pruners-ninja  py-ninja
==> 7 packages
$ spack versions ninja
==> Safe versions (already checksummed):
  master  1.12.1  1.12.0  1.11.1  1.11.0  1.10.2  1.10.1  1.10.0  1.9.0  1.8.2  1.7.2  1.6.0  kitware
==> Remote versions (not yet checksummed):
==> Warning: Found no unchecksummed versions for ninja
```

See <https://spack.readthedocs.io/en/latest/basic_usage.html#spack-versions>.

> There are two sections in the output. Safe versions are versions for which Spack has a checksum on file. It can verify that these versions are downloaded correctly.
>
> In many cases, Spack can also show you what versions are available out on the web—these are remote versions. Spack gets this information by scraping it directly from package web pages. Depending on the package and how its releases are organized, Spack may or may not be able to find remote versions.

List remote versions consumes more time, so you can list only safe versions by:

```console
$ spack versions --safe ninja
```

Add packages to the current environment:

```console
$ spack add ninja
==> Adding ninja to environment default
$ spack find
==> In environment default
==> 1 root specs
 -  ninja

==> 0 installed packages
==> 0 concretized packages to be installed (show with `spack find -c`)
```

It is not installed yet, you can check what is to be installed by:

```console
$ spack spec -lI
```

Start to install:

```console
$ spack install
...
==> ninja: Successfully installed ninja-1.12.1-urvvawqybbwfmffso5t64vw44tpuwylr
  Stage: 2.03s.  Configure: 19.96s.  Install: 0.01s.  Post-install: 0.03s.  Total: 22.08s
[+] /home/ubuntu/opt/spack-data/tree/linux-icelake/ninja-1.12.1-urvvawqybbwfmffso5t64vw44tpuwylr
==> Updating view at /home/ubuntu/opt/spack-data/environments/default/.spack-env/view
```

After installed successfully, run `spack find` again:

```console
$ spack find
==> In environment default
==> 1 root specs
[+] ninja

-- linux-ubuntu22.04-icelake / gcc@11.4.0 -----------------------
berkeley-db@18.1.40  expat@2.7.1     gmake@4.4.1    libiconv@1.18   ncurses@6.5    perl@5.40.0    python@3.13.2  sqlite@3.46.0         xz@5.6.3
bzip2@1.0.8          gdbm@1.23       libbsd@0.12.2  libmd@1.1.0     ninja@1.12.1   pigz@2.8       re2c@3.1       tar@1.35              zlib-ng@2.2.4
diffutils@3.10       gettext@0.23.1  libffi@3.4.7   libxml2@2.13.5  openssl@3.4.1  pkgconf@2.3.0  readline@8.2   util-linux-uuid@2.41  zstd@1.5.7

-- linux-ubuntu22.04-icelake / no compiler ----------------------
ca-certificates-mozilla@2025-02-25  compiler-wrapper@1.0  gcc@11.4.0  gcc-runtime@11.4.0  glibc@2.35
==> 32 installed packages
==> 0 concretized packages to be installed (show with `spack find -c`)
```

## modules

Show configs in section `modules`:

```console
$ spack config get modules
```

Configure modules (use Lmod):

```console
$ spack config add modules:default:roots:tcl:~/opt/spack-data/modules
$ spack config add modules:default:roots:lmod:~/opt/spack-data/lmod
$ spack config add modules:default:enable:lmod
$ spack config remove modules:default:enable:tcl
```

Generate module files:

```console
$ spack module lmod refresh
```

:::{tip}
You can install Lmod by Spack:

```console
$ spack add lmod
$ spack install
```

Source the init script of Lmod:

```console
$ . ${SPACK_ENV}/.spack-env/view/lmod/lmod/init/profile
```

:::

Suppose [Lmod](project:lmod.md) has been installed, the modules can be used by:

```console
$ ml use ~/opt/spack-data/lmod/linux-ubuntu22.04-x86_64/Core
$ ml use ~/opt/spack-data/lmod/linux-ubuntu22.04-x86_64/gcc/11.4.0
```

## Mirror

```console
$ mkdir ~/opt/spack-mirror
$ spack mirror create -d ~/opt/spack-mirror --all
```

## Build Cache

Spack buildcache is almost the same as mirror, but contains only prebuilt binaries.

Add a mirror:

```console
$ export TOKEN=xxxxxxxxxxxxxxxx
$ spack mirror add --unsigned --oci-username lasyard --oci-password-variable TOKEN github oci://ghcr.io/lasyard/spack-built
```

Show mirrors:

```console
$ spack mirror list
github       [sb] oci://ghcr.io/lasyard/spack-built
spack-public [s ] https://mirror.spack.io
```

Push to mirror `github` the prebuilt binaries:

```console
$ spack buildcache push --update-index github
```

If `--update-index` is omitted in the above command, you can do:

```console
$ spack buildcache update-index github
```

Then you can check the content of the buildcache:

```console
$ spack buildcache list
```

In fact, Spack will create the oci image, and put each software to an unique version of the image and tag it by the software name, version and hash.

:::{note}
You must be in an environment to push, also the prebuilt being pushed must be already installed. So you'd better do pushing before `spcak gc`, which will uninstall unnecessary packages.
:::
