# nanoGPT

<https://github.com/karpathy/nanoGPT>

## Prepare

### Program

Get the sources:

```console
$ git clone git@github.com:karpathy/nanoGPT.git
```

### Dependencies

To support old Tesla P4 (sm_61), we need old Nvidia driver:

```console
$ curl -LO https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda_12.6.0_560.28.03_linux.run
$ chmod +x cuda_12.6.0_560.28.03_linux.run
$ sudo ./cuda_12.6.0_560.28.03_linux.run
```

It is based on pytorch. Install the requirements (adapt to the CUDA version):

```console
$ pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu126
```

Other dependencies:

```console
$ pip install numpy transformers datasets tiktoken wandb tqdm
```

Check in python console:

```console
$ python
Python 3.12.5 (main, Jul 21 2026, 14:33:50) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> torch.cuda.is_available()
True
>>> torch.cuda.get_arch_list()
['sm_50', 'sm_60', 'sm_70', 'sm_75', 'sm_80', 'sm_86', 'sm_90']
```

### Dataset

```console
$ python data/shakespeare_char/prepare.py
length of dataset in characters: 1,115,394
all the unique characters: 
 !$&',-.3:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
vocab size: 65
train has 1,003,854 tokens
val has 111,540 tokens
```

## Training

```console
$ python train.py config/train_shakespeare_char.py
Overriding config with config/train_shakespeare_char.py:
...
```

If you run the above command with the too old Tesla P4, an error will be encoutered:

```text
RuntimeError: Found Tesla P4 which is too old to be supported by the triton GPU compiler, which is used as the backend. Triton only supports devices of CUDA Capability >= 7.0, but your device is of CUDA capability 6.1
```

So we need to edit the config file mentioned above, and set:

```py
compile = False
```

Which disables model compiling. Then run it again.
