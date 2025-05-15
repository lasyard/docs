# miniconda

<https://www.anaconda.com/>

## Install

Download install scripts:

```console
$ curl -LO https://repo.anaconda.com/miniconda/Miniconda3-py310_24.7.1-0-Linux-x86_64.sh
```

Install:

```console
$ chmod +x Miniconda3-py310_24.7.1-0-Linux-x86_64.sh
$ ./Miniconda3-py310_24.7.1-0-Linux-x86_64.sh

Welcome to Miniconda3 py310_24.7.1-0

In order to continue the installation process, please review the license
agreement.
Please, press ENTER to continue
...
```

Miniconda is installed into directory `~/miniconda3` by default. Run the following command to init it:

```console
$ ~/miniconda3/bin/conda init
no change     /home/ubuntu/miniconda3/condabin/conda
no change     /home/ubuntu/miniconda3/bin/conda
no change     /home/ubuntu/miniconda3/bin/conda-env
no change     /home/ubuntu/miniconda3/bin/activate
no change     /home/ubuntu/miniconda3/bin/deactivate
no change     /home/ubuntu/miniconda3/etc/profile.d/conda.sh
no change     /home/ubuntu/miniconda3/etc/fish/conf.d/conda.fish
no change     /home/ubuntu/miniconda3/shell/condabin/Conda.psm1
no change     /home/ubuntu/miniconda3/shell/condabin/conda-hook.ps1
no change     /home/ubuntu/miniconda3/lib/python3.10/site-packages/xontrib/conda.xsh
no change     /home/ubuntu/miniconda3/etc/profile.d/conda.csh
modified      /home/ubuntu/.bashrc

==> For changes to take effect, close and re-open your current shell. <==
```

For the env `PATH` is not set correctly by now, you must use full path to invoke it.

After re-login, check the version:

```console
$ conda -V
conda 24.7.1
```

Show info about conda:

```console
$ conda info

     active environment : base
    active env location : /home/ubuntu/miniconda3
            shell level : 1
       user config file : /home/ubuntu/.condarc
 populated config files : 
          conda version : 24.7.1
    conda-build version : not installed
         python version : 3.10.14.final.0
                 solver : libmamba (default)
       virtual packages : __archspec=1=icelake
                          __conda=24.7.1=0
                          __cuda=12.6=0
                          __glibc=2.35=0
                          __linux=5.15.0=0
                          __unix=0=0
       base environment : /home/ubuntu/miniconda3  (writable)
      conda av data dir : /home/ubuntu/miniconda3/etc/conda
  conda av metadata url : None
           channel URLs : https://repo.anaconda.com/pkgs/main/linux-64
                          https://repo.anaconda.com/pkgs/main/noarch
                          https://repo.anaconda.com/pkgs/r/linux-64
                          https://repo.anaconda.com/pkgs/r/noarch
          package cache : /home/ubuntu/miniconda3/pkgs
                          /home/ubuntu/.conda/pkgs
       envs directories : /home/ubuntu/miniconda3/envs
                          /home/ubuntu/.conda/envs
               platform : linux-64
             user-agent : conda/24.7.1 requests/2.32.3 CPython/3.10.14 Linux/5.15.0-139-generic ubuntu/22.04.5 glibc/2.35 solver/libmamba conda-libmamba-solver/24.7.0 libmambapy/1.5.8 aau/0.4.4 c/. s/. e/.
                UID:GID : 1000:1000
             netrc file : None
           offline mode : False
```
